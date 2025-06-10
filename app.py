import streamlit as st
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


# Set page configuration for full-screen layout
st.set_page_config(
    page_title="Cold Email Sender",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Custom CSS for styling
st.markdown("""
    <style>
    .vibrant-header {
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .vibrant-title {
        text-align: center;
        margin: 0;
    }
    .template-tab {
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .template-tab:hover {
        background-color: #f0f2f6;
        transform: translateY(-2px);
    }
    .template-tab.active {
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .template-tab h3 {
        margin: 5px 0;
        font-size: 1.1rem;
    }
    .template-tab p {
        margin: 3px 0;
        font-size: 0.85rem;
        color: inherit;
    }
    .footer {
        text-align: center;
        padding: 1rem;
        color: #6c757d;
        font-size: 0.9rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: 10px 15px;
        border-radius: 8px !important;
        background-color: #f0f2f6 !important;
        margin: 0 5px !important;
        color: #333 !important; /* <-- Dark gray text */
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6e8efb, #a777e3) !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="vibrant-header">
        <h1 class="vibrant-title">Cold Email Sender</h1>
    </div>
""", unsafe_allow_html=True)

# Get credentials from secrets
sender_email = st.secrets["email"]["sender_email"]
sender_password = st.secrets["email"]["sender_password"]
predefined_pdf_path = st.secrets.get("attachment", {}).get("file_path", "")

# Initialize variables for attachment
if 'attachment_source' not in st.session_state:
    st.session_state.attachment_source = "predefined"

# Predefined templates
templates = [
    {
        "name": "📊 Data Analyst",
        "subject": "Application for Data Analyst Role",
        "body": """Dear Hiring Team,

I hope this message finds you well.

I am writing to express my interest in a Data Analyst role at your organization. I have completed my B.Tech in Computer Science Engineering and have worked on several real-world data projects where I extracted insights, built dashboards, and helped convert data into actionable decisions.

Here’s a quick overview of what I bring:

Worked with healthcare datasets during my IIT Jodhpur research internship, using Python, SQL, Pandas, and BERT to extract and analyze structured and unstructured data.

Developed an Incident Intelligence Platform for live issue tracking and trend analysis using Streamlit, NLP, and PyTorch.

Built dashboards and visualizations using Power BI, Tableau, Matplotlib, and Plotly for better data storytelling.

Experienced with ETL pipelines, data preprocessing, feature engineering, and time-series analysis.

Strong command over tools like Excel, SQL, Pandas, NumPy, Scikit-learn, and Git, with a focus on building clean, explainable models.

I have attached my resume for your reference and would be happy to discuss how I can contribute to your team.

Warm regards,  
Hardik Chhipa  
Ph: +91 9460626737"""
    },
    {
        "name": "🤖 Data Scientist",
        "subject": "Application for Data Scientist Role",
        "body": """Dear Hiring Team,

I’m reaching out to express my interest in a Data Scientist position. I hold a B.Tech in Computer Science Engineering and have hands-on experience building machine learning solutions for real-world challenges across healthcare, risk analytics, and NLP.

Highlights of my background:

At IIT Jodhpur, I worked on extracting insights from medical data using BERT, BioBERT, BYOL, and SQL, improving model performance and scalability.

Built ClearSight.AI, a real-time diabetic retinopathy detection system for edge devices using Dense CNNs, Knowledge Distillation, and TensorFlow – achieving 98.39% accuracy.

Developed a multilingual AI chatbot (DAKSHAAB) for patient triage using Hugging Face Transformers, NLTK, and PyTorch.

Comfortable with EDA, model tuning, feature engineering, evaluation metrics, and deploying AI systems using Streamlit and FastAPI.

Published work in IEEE and ASME conferences, showing strong communication and research skills.

I’ve attached my resume and would be happy to discuss how I can contribute to your team.

Sincerely,  
Hardik Chhipa  
Ph: +91 9460626737"""
    },
    {
        "name": "⚙️ ML Engineer",
        "subject": "Application for Machine Learning Engineer/Intern Role",
        "body": """Dear Hiring Team,

I hope you're doing well. I am writing to apply for a Machine Learning Engineer or Internship role. I recently graduated with a B.Tech in Computer Science Engineering and have worked on various end-to-end ML projects with a strong focus on efficiency and accuracy.

Here’s a quick snapshot of my experience:

Built MLVICX during my internship at IIT Jodhpur to improve chest X-ray analysis using BYOL, VICReg, and contrastive learning.

Developed ClearSight.AI, a lightweight DR detection system that runs on edge devices, combining Dense CNNs, data augmentation, and TensorFlow Lite.

Created multilingual NLP pipelines and chatbots using Transformers, NLTK, and PyTorch, with experience fine-tuning models on domain-specific data.

Skilled in Python, Scikit-learn, TensorFlow, PyTorch, Pandas, NumPy, and visualization libraries.

Comfortable working with large datasets, feature engineering, and deploying ML apps via Streamlit, Docker, and FastAPI.

I’ve attached my resume and would love to connect to discuss this further.

Best,
Hardik Chhipa
Ph: +91 9460626737"""
    }
]

# Initialize session state for template tracking
if 'current_template' not in st.session_state:
    st.session_state.current_template = templates[0]
    st.session_state.email_subject = templates[0]['subject']
    st.session_state.email_body = templates[0]['body']

# --- Recipient Input ---
st.markdown("### 📬 Recipient List")
recipients_input = st.text_area(
    "Enter email addresses separated by commas:",
    placeholder="example1@gmail.com, example2@domain.com, ...",
    height=300,
    label_visibility="collapsed"
)

st.markdown("**ℹ️ Using sender account:**")
st.info(f"`{sender_email}`")

# --- Email Templates ---
st.markdown("### ✨ Email Templates")

tab_titles = [t["name"] for t in templates]
tabs = st.tabs(tab_titles)

for i, tab in enumerate(tabs):
    with tab:
        st.markdown(f"**Subject:** {templates[i]['subject']}")
        st.markdown("**Body:**")
        st.text_area("", value=templates[i]['body'], height=300, key=f"template_{i}", label_visibility="collapsed")
        
        if st.button(f"Use This Template", key=f"btn_{i}", use_container_width=True):
            st.session_state.current_template = templates[i]
            st.session_state.email_subject = templates[i]['subject']
            st.session_state.email_body = templates[i]['body']
            st.rerun()

st.markdown("---")
st.markdown(f"**Selected Template:** `{st.session_state.current_template['name']}`")

# --- Email Form ---
with st.form("email_form", border=True):
    subject = st.text_input("Subject:", value=st.session_state.email_subject)
    body = st.text_area("Message Body:", value=st.session_state.email_body, height=250)

    st.session_state.email_subject = subject
    st.session_state.email_body = body

    st.markdown("---")

    attach_pdf = st.checkbox("Attach Resume file", value=True)

    if attach_pdf:
        source = st.radio(
            "Attachment source:",
            options=["Use predefined resume", "Upload custom file"],
            index=0 if st.session_state.get("attachment_source", "Use predefined resume") == "Use predefined resume" else 1,
            horizontal=True,
            key="source_selector"
        )

        # Store the selected option in session state
        st.session_state.attachment_source = source

        if source == "Use predefined resume":
            if predefined_pdf_path and os.path.exists(predefined_pdf_path):
                st.success(f"Resume ready to attach: {os.path.basename(predefined_pdf_path)}")
            else:
                st.error("PDF file not found! Check secrets.toml configuration")

        elif source == "Upload custom file":
            uploaded_file = st.file_uploader(
                "Upload your file",
                type=["pdf", "doc", "docx", "txt", "jpg", "png", "jpeg"],
                key="file_uploader"
            )
            if uploaded_file:
                st.session_state.uploaded_file = uploaded_file
                st.success(f"Ready to attach: {uploaded_file.name}")
            else:
                st.warning("Please upload a file or switch to predefined resume")


    with st.expander("⚙️ Advanced Options", expanded=False):
        cc = st.text_input("CC (optional):", placeholder="cc@example.com")
        bcc = st.text_input("BCC (optional):", placeholder="bcc@example.com")

    submitted = st.form_submit_button("🚀 SEND EMAILS", use_container_width=True)

# --- Process Email Sending ---
if submitted:
    if not recipients_input or not subject or not body:
        st.error("❌ Please fill all required fields!")
    else:
        try:
            recipients = [email.strip() for email in recipients_input.split(',') if email.strip()]
            if cc:
                recipients.append(cc.strip())
            if bcc:
                recipients.append(bcc.strip())

            status_container = st.container()
            progress_bar = st.progress(0)
            status_text = st.empty()

            with st.spinner("🔑 Connecting to Gmail server..."):
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)

            success_count = 0
            error_count = 0
            failed_emails = []
            total = len(recipients)

            # Prepare attachment
            pdf_attachment = None
            if attach_pdf:
                try:
                    if st.session_state.attachment_source == "Use predefined resume":
                        if predefined_pdf_path and os.path.exists(predefined_pdf_path):
                            with open(predefined_pdf_path, "rb") as f:
                                pdf_data = f.read()
                            pdf_name = os.path.basename(predefined_pdf_path)
                        else:
                            st.error("Predefined PDF not found. Skipping attachment.")
                            attach_pdf = False
                    else:
                        if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
                            pdf_data = st.session_state.uploaded_file.getvalue()
                            pdf_name = st.session_state.uploaded_file.name
                        else:
                            st.error("No file uploaded. Skipping attachment.")
                            attach_pdf = False

                    if attach_pdf:
                        pdf_attachment = MIMEApplication(pdf_data, Name=pdf_name)
                        pdf_attachment['Content-Disposition'] = f'attachment; filename="{pdf_name}"'
                except Exception as e:
                    st.error(f"Failed to prepare attachment: {str(e)}")
                    attach_pdf = False

            for i, receiver_email in enumerate(recipients):
                try:
                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = receiver_email
                    msg["Subject"] = subject

                    msg.attach(MIMEText(body, "plain"))

                    if attach_pdf and pdf_attachment:
                        msg.attach(pdf_attachment)

                    server.sendmail(sender_email, receiver_email, msg.as_string())
                    success_count += 1
                    status_container.success(f"✅ Sent to {receiver_email}")
                except Exception as e:
                    error_count += 1
                    failed_emails.append((receiver_email, str(e)))
                    status_container.error(f"❌ Failed to send to {receiver_email}: {str(e)}")

                progress = (i + 1) / total
                progress_bar.progress(progress)
                status_text.info(f"**Progress:** {i+1}/{total} emails | ✅ {success_count} sent | ❌ {error_count} errors")

            progress_bar.empty()
            status_text.empty()

            if success_count > 0:
                st.success(f"## ✅ Successfully sent {success_count}/{total} emails!")

            if error_count > 0:
                st.error(f"## ❌ Failed to send {error_count} emails")
                with st.expander("⚠️ Failed Email Details", expanded=True):
                    st.markdown('<div class="error-box">', unsafe_allow_html=True)
                    st.markdown("### Failed Emails:")
                    for email, error in failed_emails:
                        st.error(f"**{email}**: `{error}`")
                    st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"## 🔐 Authentication failed: {str(e)}")
            st.info("""
                **Troubleshooting Tips:**
                1. Verify your credentials in secrets.toml  
                2. Ensure you're using an App Password if 2FA is enabled  
                3. Check if 'Less Secure Apps' is enabled in Google Account  
            """)
        finally:
            try:
                server.quit()
            except:
                pass

# --- Footer ---
st.markdown("---")
st.markdown('<div class="footer">Cold Email Sender | Secure Gmail Integration</div>', unsafe_allow_html=True)
