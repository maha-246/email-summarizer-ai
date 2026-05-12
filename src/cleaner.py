import re

def clean_text(text):
    """
    Strips whitespace, normalizes line endings, replaces tabs with spaces,
    and collapses excessive blank lines.
    """
    if not text:
        return ""
    
    # Replace tabs with spaces
    text = text.replace("\t", " ")
    
    # Normalize line endings to \n
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    
    # Collapse 3+ newlines into 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()
