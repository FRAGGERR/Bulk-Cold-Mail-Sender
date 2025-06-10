# Cold Email Sender - Streamlit Application

## Overview
Professional email automation tool for sending personalized cold emails with attachments to multiple recipients using Gmail's SMTP server.

## Features
- **Multi-recipient emailing**
- **Professional templates** (Data Analyst/Data Scientist/ML Engineer)
- **Resume attachment** (predefined or custom upload)
- **Real-time progress tracking**
- **CC/BCC support**
- **Email customization**
- **Authentication error handling**

## Setup
### 1. Install dependencies
```bash
pip install streamlit
```

### 2. Configure secrets.toml
Create .streamlit/secrets.toml with:

toml
[email]
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"

[attachment]
file_path = "path/to/resume.pdf"

### 3. Gmail Configuration
- Enable "Less secure app access"

- Create App Password if using 2FA

### 4. Run application
```bash
streamlit run app.py
```
