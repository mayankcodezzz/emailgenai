import json
import os
import google.generativeai as genai
from app.utils.exceptions import GeminiAPIError
from app.config.config import Config
from app.utils.logger import setup_logger

genai.configure(api_key=Config.GEMINI_API_KEY)

with open(os.path.join(os.path.dirname(__file__), '../config/prompts.json'), 'r', encoding='utf-8') as f:
    PROMPTS = json.load(f)

logger = setup_logger('gemini', 'logs/gemini.log')

def extract_first_name(email_or_name):
    logger.debug("Extracting first name from: %s", email_or_name)
    if '@' in email_or_name:
        name_part = email_or_name.split('@')[0]
    else:
        name_part = email_or_name
    name = ''.join(c for c in name_part if c.isalpha() or c.isspace())
    first_name = name.split()[0].capitalize() if name else "Friend"
    logger.debug("Extracted first name: %s", first_name)
    return first_name

def generate_email_content(prompt, tone, detail_level, thread_history=None, recipient_name="Recipient", sender_name="Sender"):
    logger.debug("Generating email content with prompt: %s, tone: %s", prompt, tone)
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        is_reply = thread_history is not None
        prompt_type = "reply_email" if is_reply else "new_email"
        
        recipient_first_name = extract_first_name(recipient_name)
        sender_first_name = extract_first_name(sender_name) if sender_name != "Your Name" else "Mayank"
        
        prompt_vars = {
            "context": prompt if prompt else "General message",
            "tone": tone,
            "detail_level": detail_level,
            "recipient_first_name": recipient_first_name,
            "sender_first_name": sender_first_name
        }
        
        if is_reply:
            history_str = "\n".join([f"From: {msg['sender']}\nSubject: {msg['subject']}\nBody: {msg['body']}"
                                   for msg in thread_history])
            prompt_vars["thread_history"] = history_str
        
        system_prompt = PROMPTS[prompt_type]["system_prompt"]
        user_prompt = PROMPTS[prompt_type]["user_prompt"].format(**prompt_vars)
        
        response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        
        if not response.text:
            raise GeminiAPIError("Empty response from Gemini API")
            
        email_content = response.text.strip()
        logger.info("Email content generated successfully in %s tone", tone)
        return email_content
        
    except Exception as e:
        logger.error("Error generating content: %s", str(e))
        raise GeminiAPIError(f"Failed to generate email content: {str(e)}")