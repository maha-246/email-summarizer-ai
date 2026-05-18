import re
from src.logger import logger

def detect_html(text):
    """
    Simple check for HTML tags.
    """
    if not text:
        return False
    # Look for common HTML tags or structures
    return bool(re.search(r'<(?:[a-z1-6]+|/[a-z1-6]+)\s*[^>]*>', text, re.IGNORECASE))

def clean_text(text):
    """
    Strips whitespace, normalizes line endings, replaces tabs with spaces,
    collapses excessive blank lines, and detects HTML.
    Returns: (cleaned_text, html_detected)
    """
    if not text:
        return "", False
    
    actions = []
    
    # Detect HTML before cleaning
    html_detected = detect_html(text)
    if html_detected:
        actions.append("HTML detected")
    
    # 1. Normalize line endings to \n
    if "\r" in text:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        actions.append("normalized line endings")
    
    # 2. Replace tabs with spaces
    if "\t" in text:
        text = text.replace("\t", "    ")
        actions.append("replaced tabs with spaces")
    
    # 3. Collapse 4+ newlines into 3
    if re.search(r'\n{4,}', text):
        text = re.sub(r'\n{4,}', '\n\n\n', text)
        actions.append("collapsed excessive blank lines")
    
    # 4. Collapse repeated spaces (2+)
    if re.search(r' {2,}', text):
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            cleaned_line = re.sub(r' {2,}', ' ', line)
            cleaned_lines.append(cleaned_line)
        text = "\n".join(cleaned_lines)
        actions.append("collapsed repeated spaces")
    
    # 5. Final strip
    text = text.strip()
    
    if actions:
        logger.info(f"Cleanup performed: {', '.join(actions)}")
    
    return text, html_detected
