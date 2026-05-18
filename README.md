# 📧 Email Summary Assistant

A powerful, modular Streamlit application that uses AI to transform long, cluttered emails into structured, actionable summaries. It features a robust multi-provider fallback system (Gemini & Groq) to ensure high availability.

## ✨ Features

- **Structured Summarization**: Extracts key details, priority, action items, and deadlines into a clean JSON-based UI.
- **Dual AI Providers**: Uses **Google Gemini** as the primary engine with an automatic fallback to **Groq (Llama 3.1)** if Gemini's quota is exceeded or servers are overloaded.
- **Privacy First**: Truncates long emails and includes privacy warnings. Sensitive information detection flags passwords, OTPs, and private links.
- **Mock Mode**: Built-in testing mode to simulate AI responses without using API credits.
- **Modular Architecture**: Cleanly separated into Frontend, Backend, Prompts, and Config modules for easy maintenance.

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/maha-246/email-summarizer-ai.git
cd email-summarizer-ai
```

### 2. Set Up Environment
Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the root directory and add your keys:
```env
GEMINI_API_KEY=your_gemini_key_here
GROQ_API_KEY=your_groq_key_here

# Optional Settings
GEMINI_MODEL=gemini-3.1-flash-lite-preview
GROQ_MODEL=llama-3.1-8b-instant
MOCK_MODE=false
```

### 4. Run the App
```bash
streamlit run app.py
```

## 📁 Project Structure

- `app.py`: Streamlit entry point (UI logic only).
- `config.py`: Root-level configuration and environment management.
- `.env`: Private environment variables (not tracked).
- `.env.example`: Template for environment variables.
- `src/`: Core logic package.
    - `summarizer.py`: Orchestrates the summarization pipeline.
    - `llm_client.py`: Handles Gemini and Groq API interactions.
    - `prompts.py`: AI system instructions and prompt templates.
    - `cleaner.py`: Text normalization and cleaning.
    - `validator.py`: JSON parsing and field validation.
    - `logger.py`: Safe, centralized logging.
    - `redactor.py`: (Placeholder) Sensitive info redaction.
    - `parser.py`: (Placeholder) File parsing logic.
    - `chunker.py`: (Placeholder) Text chunking logic.


