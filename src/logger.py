import logging
import sys

def setup_logger():
    """
    Sets up a basic logger that outputs to stdout.
    Safety: Do not log email bodies, prompts, or API keys.
    """
    logger = logging.getLogger("email-summarizer")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()
