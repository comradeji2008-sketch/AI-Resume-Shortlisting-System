cat > README.md <<'EOF'
# AI-Powered Resume Shortlisting System

An LLM-powered Python application for automated resume parsing, job description analysis, candidate evaluation and shortlisting.

## Features
- Job description analysis and structured information extraction.
- PDF and DOCX resume processing.
- AI-powered candidate information extraction.
- Skill and qualification matching.
- Candidate match scoring and ranking.

## Technologies
- Python
- Groq API
- GPT-OSS 120B
- Pydantic
- PyPDF
- python-docx

## Setup

1. Clone this repository.
2. Create a virtual environment:

   python -m venv .venv

3. Activate it:

   source .venv/bin/activate

4. Install dependencies:

   pip install -r requirements.txt

5. Create a `.env` file and add your Groq API key:

   GROQ_API_KEY=your_api_key

6. Add PDF or DOCX resumes to the `resumes/` folder.

7. Run:

   python resumecall.py

## Project Status

Backend prototype. Frontend integration and further evaluation are planned.
EOF