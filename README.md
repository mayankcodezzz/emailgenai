# MailGenix


https://github.com/user-attachments/assets/6a4488b9-00bd-4d83-bf05-f62630614ac1


## Overview

**MailGenix** is an AI-powered email client with a futuristic dark theme, enabling users to generate professional emails, manage their Gmail inbox, and reply smartly using Gemini AI and Gmail API.

## Pipeline

1. **Authentication**: Sign in securely via Google OAuth2 to access Gmail.
2. **Inbox Management**: Fetch and display emails and thread history using Gmail API.
3. **Email Generation**: Input context, tone, and detail level to generate emails or replies with Gemini AI.
4. **Compose & Send**: Format emails with bold/italic options and send via Gmail API.
5. **UI Interaction**: Navigate a sleek, neon-themed interface with glowing effects for an immersive experience.

## Tech Stack

- **Backend**: Flask (Python) for routing and API integration.
- **Frontend**: HTML, CSS (Bootstrap), JavaScript for a responsive, futuristic UI.
- **APIs**:
  - **Gmail API**: For email fetching, sending, and thread management.
  - **Gemini AI**: For generating email content with customizable tones.
- **Styling**: Custom CSS with `Exo 2` font, dark theme, and neon glow effects.
- **Environment**: Managed via `.env` for secure API keys and credentials.

## Setup

1. Clone the repo: `git clone https://github.com/yourusername/MailGenix.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Add `.env` with API keys and `credentials.json` for Gmail API.
4. Run: `python run.py` and visit `http://localhost:5000`.
