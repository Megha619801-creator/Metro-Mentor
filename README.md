# MetroMentor AI - Flask Demo

**Purpose**: A simple Flask app that answers questions international students may have about why to choose Metropolia UAS and why its teachers/programs stand out. This is a demo suitable for the Metropolia AI dev project application.

## Features
- Single-page web UI with text input
- Calls `ai.generate_answer()` that uses OpenAI when `OPENAI_API_KEY` is set, otherwise falls back to an offline responder
- Simple, modern UI

## Files
- `app.py` - Flask server
- `ai.py` - AI integration (OpenAI + fallback)
- `templates/index.html` - Frontend page
- `static/style.css` - Styles
- `requirements.txt` - Python packages

## Setup (local)
1. Install Python 3.8+ and create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. (Optional) Set your OpenAI API key to enable LLM answers:
   ```bash
   export OPENAI_API_KEY="sk-..."
   # optionally choose model:
   export OPENAI_MODEL="gpt-3.5-turbo"
   ```
3. Run the app:
   ```bash
   python app.py
   ```
   Visit http://127.0.0.1:5000
   # C:\Users\mahat\OneDrive\Desktop\Metromentor\venv\Scripts\Activate.ps1
   # Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   # $env:OPENAI_API_KEY="YOUR_KEY_HERE"
   # $env:OPENAI_MODEL="gpt-4o-mini" ///////$env:OPENAI_MODEL="gpt-4o"
   # python app.py

   FOR OPENAI API KEY NEED TO INSTALL DOTENV FROM TERMINAL AND THEN MAKE SEPARATE FILE .ENV FOR STORING OF API KEY,
   Go to:

👉 https://platform.openai.com/settings/organization/api-keys (to generate api key)
  for gemini api key (its free touse )
  go to googlestudioai/api-keys and create  api key and put in project (you can use versions of gemini according to the list available )
## How it works
- `app.py` provides an `/ask` endpoint. The frontend sends a JSON POST with `question`.
- `ai.py` tries to call OpenAI ChatCompletion. If no API key is present, a safe local fallback delivers helpful, generic answers.
- The UI displays the answer.

