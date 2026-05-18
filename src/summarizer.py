import time
import config
from src.cleaner import clean_text
from src.prompts import get_summarization_prompt
from src.llm_client import get_llm_response
from src.validator import clean_and_parse_json, validate_summary_data
from src.logger import logger

def summarize_email(email_content):
    """
    Main orchestration function for email summarization.
    Steps: Clean -> Validate -> Prompt -> LLM -> Parse -> Validate JSON -> Return
    Returns: (data, provider, error_message, warning_message)
    """
    warning_message = None
    
    # 1. Cleaning & Initial Validation
    cleaned_content, html_detected = clean_text(email_content)
    
    if not cleaned_content:
        return None, None, "Please paste an email body first.", None
    
    if len(cleaned_content) < config.MIN_CHARS:
        return None, None, None, "The email text is too short to summarize."

    if html_detected:
        warning_message = "HTML-like content was detected. Some formatting may be simplified."

    if len(cleaned_content) > config.MAX_CHARS:
        cleaned_content = cleaned_content[:config.MAX_CHARS]
        truncation_msg = f"Email truncated to {config.MAX_CHARS} characters for free-tier compatibility."
        warning_message = f"{warning_message} | {truncation_msg}" if warning_message else truncation_msg

    # 2. Mock Mode Support
    if config.MOCK_MODE:
        logger.info("Running in MOCK MODE")
        time.sleep(1) # Simulate lag
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

    # 3. LLM Pipeline
    try:
        prompt = get_summarization_prompt(cleaned_content)
        response_text, provider = get_llm_response(prompt)
        
        # 4. Parsing & Final Validation
        raw_data = clean_and_parse_json(response_text)
        if not raw_data:
            return None, provider, "The AI returned an invalid JSON response. Please try again.", warning_message
        
        final_data = validate_summary_data(raw_data)
        return final_data, provider, None, warning_message

    except Exception as e:
        logger.error(f"Summarization pipeline failed: {e}")
        return None, None, f"Error: {str(e)}", None
