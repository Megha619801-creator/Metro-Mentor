import os
import google.generativeai as genai

def generate_answer(question: str) -> str:
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if gemini_api_key:
        try:
            # Configure Gemini
            genai.configure(api_key=gemini_api_key)

            # Choose a Gemini model (flash = faster, pro = deeper reasoning)
            model_name = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
            model = genai.GenerativeModel(model_name)

            # Generate response
            response = model.generate_content(
                f"You are MetroMentor AI, an assistant that explains why Metropolia UAS is a good choice for international students. "
                f"Provide clear, friendly, and fact-based answers.\n\nUser question: {question}"
            )

            return response.text.strip()
        except Exception as e:
            return offline_answer(question, note=f" (Gemini call failed: {e})")
    else:
        return offline_answer(question, note=" (no GEMINI_API_KEY found)")


def offline_answer(question: str, note: str = "") -> str:
    q = question.lower()
    if "why metropolia" in q or "why choose metropolia" in q or "choose metropolia" in q:
        return ("Metropolia is a practice-oriented university of applied sciences with strong links to industry and a modern, international learning environment. "
                "It focuses on applied projects, cooperative education, and close ties with local and international companies — which makes studies highly job-relevant for international students." + note)
    if "teacher" in q or "teachers" in q or "qualifications" in q:
        return ("Metropolia's teaching staff typically combine academic qualifications with real-world industry experience. "
                "Many teachers have advanced degrees and active ties to industry projects, which helps connect teaching with practical skills and internships." + note)
    if "compare" in q or "better than" in q or "vs" in q:
        return ("Compared to many traditional universities, Metropolia emphasizes applied learning, smaller project-based courses, and strong links to local businesses. "
                "That can be an advantage for students seeking practical experience and employability." + note)
    return ("MetroMentor AI: Metropolia offers practical, project-based education, strong industry ties, and an international environment. "
            "If you want specific program comparisons or teacher profiles, ask about a particular field or program." + note)
