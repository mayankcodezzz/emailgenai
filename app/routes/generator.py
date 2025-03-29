from flask import Blueprint, request, jsonify
from app.services.gemini_service import generate_email_content
from app.services.gmail_service import get_thread
from app.utils.exceptions import GeminiAPIError, GmailAPIError
from app.utils.logger import setup_logger

bp = Blueprint('generator', __name__)
logger = setup_logger('generator', 'logs/generator.log')

@bp.route('/generate', methods=['POST'])
def generate():
    logger.debug("Received generate request")
    data = request.json
    prompt = data.get('prompt', '')
    tone = data.get('tone', 'normal')
    detail_level = data.get('detail_level', 'simple')
    thread_id = data.get('thread_id')
    recipient_name = data.get('recipient_name', 'Recipient')
    sender_name = data.get('sender_name', 'Sender')
    
    logger.debug("Generating email with tone: %s, detail: %s", tone, detail_level)
    try:
        thread_history = get_thread(thread_id) if thread_id else None
        content = generate_email_content(
            prompt=prompt,
            tone=tone,
            detail_level=detail_level,
            thread_history=thread_history,
            recipient_name=recipient_name,
            sender_name=sender_name
        )
        
        parts = content.split('---', 1)
        if len(parts) != 2:
            raise ValueError("Invalid email format from Gemini")
        
        subject = parts[0].replace('Subject: ', '').strip()
        body = parts[1].strip()
        
        logger.info("Email content generated successfully")
        return jsonify({
            'subject': subject,
            'body': body
        })
    except (GeminiAPIError, GmailAPIError, ValueError) as e:
        logger.error("Generation error: %s", str(e))
        return jsonify({'error': str(e)}), 500