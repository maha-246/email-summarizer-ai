from google import genai
from groq import Groq
import config
from src.logger import logger

def call_gemini(prompt):
    """
    Handles Gemini API call.
    """
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=config.GEMINI_MODEL, 
            contents=prompt
        )
        return response.text, "Gemini"
    except Exception as e:
        logger.warning(f"Gemini API call failed: {e}")
        raise e

def call_groq(prompt):
    """
    Handles Groq API call.
    """
    try:
        groq_client = Groq(api_key=config.GROQ_API_KEY)
        completion = groq_client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content, "Groq"
    except Exception as e:
        logger.error(f"Groq API call failed: {e}")
        raise e

def get_llm_response(prompt):
    """
    Tries Gemini first, falls back to Groq on specific errors.
    Returns: (response_text, provider)
    """
    # Try Gemini
    if config.GEMINI_API_KEY:
        try:
            return call_gemini(prompt)
        except Exception as e:
            err_str = str(e).lower()
            # Check for rate limit / quota / server errors
            is_fallback_error = any(key in err_str for key in [
                "429", "503", "resource_exhausted", "quota", 
                "rate", "unavailable", "demand"
            ])
            
            if not is_fallback_error:
                raise e # Re-raise if it's an authentication or other fatal error
            
            logger.info("Attempting Groq fallback...")
    
    # Fallback to Groq
    if config.GROQ_API_KEY:
        return call_groq(prompt)
    
    raise Exception("No API keys found. Please provide either a Gemini or Groq API key in your .env file.")
