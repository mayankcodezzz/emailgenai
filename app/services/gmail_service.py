import os
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from app.utils.exceptions import GmailAPIError
from app.utils.logger import setup_logger

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
logger = setup_logger('gmail', 'logs/gmail.log')

def get_gmail_service():
    logger.debug("Getting Gmail service")
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.debug("Refreshing expired credentials")
            creds.refresh(Request())
        else:
            logger.debug("Running OAuth flow")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            logger.info("New token saved")
    return build('gmail', 'v1', credentials=creds)

def fetch_emails(category='inbox'):
    logger.debug("Fetching emails for category: %s", category)
    try:
        service = get_gmail_service()
        query = '-from:me'
        results = service.users().threads().list(userId='me', q=query, maxResults=10).execute()
        threads = results.get('threads', [])
        emails = []
        for thread in threads:
            thread_data = service.users().threads().get(userId='me', id=thread['id']).execute()
            messages = thread_data['messages']
            first_msg = messages[0]
            headers = first_msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            snippet = first_msg['snippet']
            emails.append({
                'thread_id': thread['id'],
                'subject': subject,
                'sender': sender,
                'snippet': snippet,
                'count': len(messages)
            })
        logger.info("Emails fetched successfully for %s", category)
        return emails
    except Exception as e:
        logger.error("Error fetching emails: %s", str(e))
        raise GmailAPIError(f"Failed to fetch emails: {str(e)}")

def get_thread(thread_id):
    logger.debug("Fetching thread: %s", thread_id)
    try:
        service = get_gmail_service()
        thread = service.users().threads().get(userId='me', id=thread_id).execute()
        messages = thread.get('messages', [])
        history = []
        for msg in messages:
            headers = msg.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            body = msg.get('snippet', 'No body content')
            history.append({'subject': subject, 'sender': sender, 'body': body})
        logger.info("Thread %s fetched successfully", thread_id)
        return history
    except Exception as e:
        logger.error("Error fetching thread %s: %s", thread_id, str(e))
        raise GmailAPIError(f"Failed to fetch thread: {str(e)}")

def send_email(to, subject, body, thread_id=None):
    logger.debug("Sending email to %s, thread_id: %s", to, thread_id)
    try:
        service = get_gmail_service()
        message = MIMEText(body, 'html')
        message['to'] = to
        message['subject'] = subject
        if thread_id:
            message['threadId'] = thread_id
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw, 'threadId': thread_id}).execute()
        logger.info("Email sent successfully to %s", to)
    except Exception as e:
        logger.error("Error sending email: %s", str(e))
        raise GmailAPIError(f"Failed to send email: {str(e)}")