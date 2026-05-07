import json
import re

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
    except (json.JSONDecodeError, AttributeError):
        return None
