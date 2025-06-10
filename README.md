# 📧 Cold Email Sender — Streamlit App

A powerful and user-friendly **Streamlit** application to automate sending personalized cold emails with optional resume attachments. Ideal for job seekers targeting multiple roles such as Data Analyst, Data Scientist, and Machine Learning Engineer.

---

## 🚀 Features

- 🔐 **Secure Gmail Integration** using credentials stored in `secrets.toml`
- 🧩 **Predefined Email Templates** for common job roles
- ✍️ **Editable Subject & Message Body**
- 📎 **Attach Resume Automatically** or via Upload
- 📬 **Bulk Recipient Entry** with Progress Tracking
- 🛠️ **Advanced Options** like CC and BCC
- 📊 **Real-time Success/Error Feedback** for each email sent
- 💡 **Session State Management** for persistent user selections

---
## Setup
### 1. Install dependencies
```bash
pip install streamlit
```
### 2. Clone the Repository

```bash
git clone https://github.com/FRAGGERR/Bulk-Cold-Mail-Sender.git)=
cd app.py
```

### 3. Configure secrets.toml
Create .streamlit/secrets.toml with:

toml
[email]
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"

[attachment]
file_path = "path/to/resume.pdf"

### 4. Gmail Configuration
- Enable "Less secure app access"

- Create App Password if using 2FA

### 5. Run application
```bash
streamlit run app.py
```
