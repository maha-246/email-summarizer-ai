import json
import re
from src.logger import logger

def clean_and_parse_json(text):
    """
    Cleans markdown formatting and parses text into a JSON object.
    """
    try:
        raw_text = text.strip()
        # Remove markdown code blocks if present
        if raw_text.startswith("```"):
            match = re.search(r'```(?:json)?\s*(.*?)\s*```', raw_text, re.DOTALL)
            if match:
                raw_text = match.group(1)
        
        return json.loads(raw_text)
    except (json.JSONDecodeError, AttributeError) as e:
        logger.error(f"Failed to parse JSON: {e}")
        return None

def validate_summary_data(data):
    """
    Validates parsed JSON fields and fills safe defaults.
    """
    if not isinstance(data, dict):
        return None

    defaults = {
        "summary": "No summary provided.",
        "priority": "medium",
        "important_details": [],
        "required_action": "No action required.",
        "deadline": None,
        "sensitive_info_detected": False,
        "suggested_reply": "Thank you for your email."
    }

    # Fill missing fields
    for key, value in defaults.items():
        if key not in data:
            data[key] = value

    # Validate priority
    valid_priorities = ["high", "medium", "low"]
    if data["priority"].lower() not in valid_priorities:
        data["priority"] = "medium"
    else:
        data["priority"] = data["priority"].lower()

    return data
