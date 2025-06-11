# 📧 Cold Email Sender — Streamlit App

A powerful and user-friendly **Streamlit** application to automate sending personalized cold emails with optional resume attachments. Ideal for job seekers targeting multiple roles such as Data Analyst, Data Scientist, and Machine Learning Engineer.

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://clearsight.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)
![Firebase](https://img.shields.io/badge/firebase-a08021?style=for-the-badge&logo=firebase&logoColor=ffcd34)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)


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
pip install -r requirements.txt
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


## Screenshots

![Image](https://github.com/user-attachments/assets/a29b8b1e-6f0b-4979-8928-d27ab395e5fc)


## Deployment

To deploy this project run

```bash
  https://coldmail-sender.streamlit.app/
```

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@hardikchhipa](https://github.com/FRAGGERR)
## 🔗 Links
[![portfolio](https://img.shields.io/badge/Kaggle-000?style=for-the-badge&logo=ko-fi&logoColor=white)]([https://katherineoelsner.com/](https://www.kaggle.com/hardikchhipa28))
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/hardik-chhipa-303040242/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/HardikChhipa)
