from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.gmail_service import fetch_emails, send_email, get_thread
from app.utils.exceptions import GmailAPIError
from app.utils.logger import setup_logger

bp = Blueprint('email', __name__)
logger = setup_logger('email', 'logs/email.log')

@bp.route('/')
def index():
    logger.debug("Accessing index route")
    if 'logged_in' not in session:
        logger.info("User not logged in, redirecting to login")
        return redirect(url_for('auth.login'))
    return redirect(url_for('email.inbox'))

@bp.route('/inbox')
def inbox():
    logger.debug("Fetching inbox")
    if 'logged_in' not in session:
        logger.info("User not logged in, redirecting to login")
        return redirect(url_for('auth.login'))
    try:
        emails = fetch_emails()
        logger.info("Inbox fetched successfully")
        return render_template('inbox.html', emails=emails)
    except GmailAPIError as e:
        logger.error("Failed to fetch inbox: %s", str(e))
        return str(e), 500

@bp.route('/compose', methods=['GET', 'POST'])
def compose():
    logger.debug("Accessing compose page")
    if 'logged_in' not in session:
        logger.info("User not logged in, redirecting to login")
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        to = request.form['to']
        subject = request.form['subject']
        body = request.form['body']
        logger.debug("Sending email to %s", to)
        try:
            send_email(to, subject, body)
            logger.info("Email sent successfully to %s", to)
            return redirect(url_for('email.inbox'))
        except GmailAPIError as e:
            logger.error("Failed to send email: %s", str(e))
            return str(e), 500
    return render_template('compose.html')

@bp.route('/reply/<thread_id>', methods=['GET', 'POST'])
def reply(thread_id):
    logger.debug("Accessing reply page for thread %s", thread_id)
    if 'logged_in' not in session:
        logger.info("User not logged in, redirecting to login")
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        to = request.form['to']
        subject = request.form['subject']
        body = request.form['body']
        logger.debug("Sending reply to %s for thread %s", to, thread_id)
        try:
            send_email(to, subject, body, thread_id)
            logger.info("Reply sent successfully to %s", to)
            return redirect(url_for('email.inbox'))
        except GmailAPIError as e:
            logger.error("Failed to send reply: %s", str(e))
            return str(e), 500
    try:
        thread = get_thread(thread_id)
        logger.info("Thread %s fetched successfully", thread_id)
        return render_template('reply.html', thread_id=thread_id, thread=thread)
    except GmailAPIError as e:
        logger.error("Failed to fetch thread %s: %s", thread_id, str(e))
        return str(e), 500