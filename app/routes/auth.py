from flask import Blueprint, redirect, url_for, session, render_template
from app.services.gmail_service import get_gmail_service
from app.utils.logger import setup_logger
import os
import requests

bp = Blueprint('auth', __name__)
logger = setup_logger('auth', 'logs/auth.log')

@bp.route('/login')
def login():
    logger.debug("Accessing login page")
    if 'logged_in' in session:
        logger.info("User already logged in, redirecting to inbox")
        return redirect(url_for('email.inbox'))
    return render_template('login.html')

@bp.route('/google_login')
def google_login():
    logger.debug("Initiating Google login")
    try:
        get_gmail_service()
        session['logged_in'] = True
        logger.info("User logged in successfully")
        return redirect(url_for('email.inbox'))
    except Exception as e:
        logger.error("Login error: %s", str(e))
        return "Login failed", 500

@bp.route('/logout')
def logout():
    logger.debug("Initiating logout")
    try:
        service = get_gmail_service()
        creds = service._http.credentials
        
        if creds and creds.token:
            revoke_url = f"https://oauth2.googleapis.com/revoke?token={creds.token}"
            response = requests.post(revoke_url)
            if response.status_code == 200:
                logger.info("Google token revoked successfully")
            else:
                logger.warning("Failed to revoke token: %s", response.status_code)

        session.pop('logged_in', None)
        if os.path.exists('token.json'):
            os.remove('token.json')
            logger.info("Token file removed")
        
        logger.info("User logged out successfully")
        return redirect(url_for('auth.login'))
    except Exception as e:
        logger.error("Logout error: %s", str(e))
        session.pop('logged_in', None)
        if os.path.exists('token.json'):
            os.remove('token.json')
        return redirect(url_for('auth.login'))