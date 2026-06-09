# MIRA - Health Prediction App

A simple patient health prediction web application built with Python and Flask.

## What it does
- Add, view, edit and delete patient records
- Stores blood test values (glucose, haemoglobin, cholesterol)
- Uses Groq AI API (Llama3) to generate a health remark based on the blood test values
- Stores all data in a local SQLite database

## Tech Stack
- Python + Flask (backend)
- HTML + Bootstrap 5 (frontend)
- SQLite (database)
- Groq API with Llama3 model (AI health remarks)

## How to run

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Set up your API key
- Go to https://console.groq.com and sign up (free, no credit card)
- Create an API key
- Copy `.env.example` to `.env` and paste your key:
```
GROQ_API_KEY=your_key_here
```

### 3. Run the app
```
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Notes
- Groq API is completely free to use
- Do not commit your `.env` file to GitHub
