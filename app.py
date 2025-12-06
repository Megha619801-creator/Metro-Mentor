from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env
load_dotenv()

print("dotenv installed successfully!")

# Configure Gemini with API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("No GEMINI_API_KEY found in environment variables")

genai.configure(api_key=gemini_api_key)
# for m in genai.list_models():
#     print(m.name, "supports:", m.supported_generation_methods)

# Choose model (flash = faster, pro = deeper reasoning)
model_name = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")
model = genai.GenerativeModel(model_name)

print("Your Gemini API Key is set up and model is configured.")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///metromentor.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False, unique=False)
    answer = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Info {self.id} - {self.question[:60]}>"
# // Create  the database tables in file (create_db.py) 

def generate_answer(question: str) -> str:
    """Generate an answer using Gemini API."""
    try:
        response = model.generate_content(
            f"You are MetroMentor AI, an assistant that explains why Metropolia UAS is a good choice for international students. "
            f"Provide clear, friendly, and fact-based answers.\n\nUser question: {question}"
        )
        return response.text.strip()
    except Exception as e:
        return f"MetroMentor AI (offline fallback): Could not reach Gemini. {e}"


@app.route("/", methods=["GET"])
def index():
    # Show all saved Q/A pairs (most recent first)
    all_info = Info.query.order_by(Info.date_created.desc()).all()
    return render_template("index.html", all_info=all_info)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"error": "No question provided."}), 400

    # Check DB for an existing (case-insensitive) answer
    existing = Info.query.filter(Info.question.ilike(question)).first()
    if existing:
        return jsonify({"answer": existing.answer, "cached": True})

    # Not found in memory -> call Gemini and save result
    answer = generate_answer(question)

    try:
        info = Info(question=question, answer=answer)
        db.session.add(info)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return jsonify({"answer": answer, "cached": False})


@app.route("/history", methods=["GET"])
def history():
    # Optional JSON endpoint for stored memory
    all_info = Info.query.order_by(Info.date_created.desc()).all()
    return jsonify([
        {"id": i.id, "question": i.question, "answer": i.answer, "date_created": i.date_created.isoformat()}
        for i in all_info
    ])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
