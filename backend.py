from google import genai
from groq import Groq
from prompts import get_summarization_prompt
from utils import clean_and_parse_json
import config

def process_email(email_content):
    """
    Handles validation, truncation, and AI summarization using central config.
    Returns: (data, provider, error_message, warning_message)
    """
    # 1. Validation & Truncation
    clean_content = email_content.strip()
    warning_message = None

    if not clean_content:
        return None, None, "Please paste an email body first.", None
    
    if len(clean_content) < config.MIN_CHARS:
        return None, None, f"The email text is too short (min {config.MIN_CHARS} chars).", None

    if len(clean_content) > config.MAX_CHARS:
        clean_content = clean_content[:config.MAX_CHARS]
        warning_message = f"Email truncated to {config.MAX_CHARS} characters for free-tier compatibility."

    if config.MOCK_MODE:
        import time
        time.sleep(1) # Simulate network lag
        mock_data = {
            "summary": "This is a MOCK summary for testing. The email discussed a project deadline.",
            "priority": "high",
            "important_details": ["Mock detail 1", "Mock detail 2"],
            "required_action": "Verify if the AI logic is working.",
            "deadline": "2026-12-31",
            "sensitive_info_detected": False,
            "suggested_reply": "This is a mock suggested reply."
        }
        return mock_data, "MockProvider", None, warning_message or "Warning: Running in MOCK MODE."

    # 2. Get AI Response
    prompt = get_summarization_prompt(clean_content)
    
    # Try Gemini
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(model=config.GEMINI_MODEL, contents=prompt)
        data = clean_and_parse_json(response.text)
        if data:
            return data, "Gemini", None, warning_message
    except Exception as e:
        err_str = str(e).lower()
        # Fallback to Groq if quota/server error
        if any(key in err_str for key in ["429", "503", "resource_exhausted", "quota", "rate", "unavailable", "demand"]):
            if not config.GROQ_API_KEY:
                return None, None, "Gemini quota exceeded and no Groq fallback key found.", None
            
            try:
                groq_client = Groq(api_key=config.GROQ_API_KEY)
                completion = groq_client.chat.completions.create(
                    model=config.GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}]
                )
                data = clean_and_parse_json(completion.choices[0].message.content)
                if data:
                    return data, "Groq", None, warning_message
            except Exception as groq_e:
                return None, None, f"Both Gemini and Groq failed. Error: {groq_e}", None
        else:
            return None, None, f"Gemini Error: {e}", None

    return None, None, "The AI returned an invalid response. Please try again.", None
