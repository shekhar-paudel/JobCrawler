import requests
from dotenv import load_dotenv
import os
import re
from logs.logging_config import logger


def escape_markdown(text):
    """
    Escapes special characters for Telegram MarkdownV2 formatting.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r'\\\1', text)

def send_telegram_message(message):
    load_dotenv()
    bot_token = os.getenv("bot_token")
    chat_id = os.getenv("chat_id")
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    safe_message = escape_markdown(message)  # Escape special characters
    payload = {
        'chat_id': chat_id,
        'text': safe_message,
        'parse_mode': 'MarkdownV2'  # Optional: use 'Markdown' or 'HTML' for formatting
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        logger.info("Message sent successfully!")
    else:
        logger.info(f"Failed to send message: {response.status_code}, {response.text}")
    return response.status_code
