import os
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Set page configuration for full-screen layout
st.set_page_config(
    page_title="Cold Email Sender",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for full-screen expansion
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap');
        
        /* Vibrant Header Styles */
        .vibrant-header {
            text-align: center;
            padding: 1.5rem 0;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(106, 90, 205, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        .vibrant-title {
            font-family: 'Poppins', sans-serif;
            font-size: 3.6rem !important;
            background: linear-gradient(90deg, #ff8a00, #e52e71, #22c1c3, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 300% 300%;
            animation: gradient 8s ease infinite;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
            text-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .vibrant-subheader {
            font-size: 1.8rem !important;
            color: #c0e3f0;
            font-weight: 400;
            margin-top: 0 !important;
            text-shadow: 0 2px 8px rgba(0,0,0,0.3);
            letter-spacing: 0.5px;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50% }
            50% { background-position: 100% 50% }
            100% { background-position: 0% 50% }
        }
        
        /* Main App Styles */
        .main > div {
            padding: 1rem 3% !important;
        }
        
        [data-testid="stForm"] {
            border: 1px solid #2d5b8c;
            border-radius: 10px;
            padding: 25px;
            background: #0e1117;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        /* FIXED TEXTAREA SELECTOR */
        .stTextArea textarea {
            min-height: 300px !important;
        }
        
        .stButton button {
            width: 100%;
            background: linear-gradient(to right, #2d5b8c, #1e3c72);
            color: white;
            font-weight: bold;
            padding: 14px 28px;
            border-radius: 8px;
            font-size: 18px;
            margin-top: 15px;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 12px rgba(0,0,0,0.25);
        }
        
        .success {
            color: #4CAF50;
            font-weight: bold;
            font-size: 1.2em;
        }
        
        .error {
            color: #FF5252;
            font-weight: bold;
        }
        
        .recipients-box {
            background: rgba(45,91,140,0.15);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #7a7a7a;
        }
        
        .error-box {
            background: rgba(255, 82, 82, 0.15);
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            border: 1px solid #FF5252;
        }
        
        @media (min-width: 1200px) {
            .main > div {
                max-width: 95% !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Header with correct class names
st.markdown("""
    <div class="vibrant-header">
        <h1 class="vibrant-title">Cold Email Sender</h1>
    </div>
""", unsafe_allow_html=True)



# Get credentials from secrets
sender_email = st.secrets["email"]["sender_email"]
sender_password = st.secrets["email"]["sender_password"]

# Using columns for layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("")
    st.markdown("### Recipient List")

    recipients_input = st.text_area(
        "Enter email addresses separated by commas:",
        placeholder="example1@gmail.com, example2@domain.com, ...",
        height=300,  # Doubled height
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("**ℹ️ Using sender account:**")
    st.info(f"`{sender_email}`")


with col2:
    with st.form("email_form", border=False):
        st.markdown("### Compose Email")
        subject = st.text_input("Subject:", placeholder="Important Announcement")
        body = st.text_area("Message Body:", height=250, placeholder="Type your message here...")
        
        # PDF Attachment Section
        st.markdown("---")
        attach_pdf = st.checkbox("Attach Resume file", value=True)
        
        if attach_pdf:
            # Get PDF path from secrets
            pdf_path = st.secrets.get("attachment", {}).get("file_path", "")
            
            if pdf_path and os.path.exists(pdf_path):
                try:
                    with open(pdf_path, "rb") as f:
                        pdf_data = f.read()
                    pdf_name = os.path.basename(pdf_path)
                    st.success(f"Resume ready to attach: {pdf_name}")
                except Exception as e:
                    st.error(f"Error reading PDF: {str(e)}")
                    attach_pdf = False
            else:
                st.error("PDF file not found! Check secrets.toml configuration")
                attach_pdf = False
        
        # Advanced options
        with st.expander("⚙️ Advanced Options", expanded=False):
            cc = st.text_input("CC (optional):", placeholder="cc@example.com")
            bcc = st.text_input("BCC (optional):", placeholder="bcc@example.com")
        
        submitted = st.form_submit_button("🚀 SEND EMAILS", use_container_width=True)


# Process email sending
if submitted:
    if not recipients_input or not subject or not body:
        st.error("❌ Please fill all required fields!")
    else:
        try:
            # Parse recipients
            recipients = [email.strip() for email in recipients_input.split(',') if email.strip()]
            
            # Add CC/BCC if provided
            if cc: recipients.append(cc.strip())
            if bcc: recipients.append(bcc.strip())
            
            # Status container
            status_container = st.container()
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Connect to SMTP server
            with st.spinner("🔑 Connecting to Gmail server..."):
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)
            
            success_count = 0
            error_count = 0
            failed_emails = []  # Store failed email addresses
            total = len(recipients)
            
            # Prepare PDF attachment if enabled
            pdf_attachment = None
            if attach_pdf:
                try:
                    with open(pdf_path, "rb") as f:
                        pdf_attachment = MIMEApplication(f.read(), Name=os.path.basename(pdf_path))
                        pdf_attachment['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
                except Exception as e:
                    st.error(f"Failed to prepare PDF attachment: {str(e)}")
            
            for i, receiver_email in enumerate(recipients):
                try:
                    # Create message
                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = receiver_email
                    msg["Subject"] = subject
                    
                    # Add body text
                    msg.attach(MIMEText(body, "plain"))
                    
                    # Add PDF attachment if enabled
                    if attach_pdf and pdf_attachment:
                        msg.attach(pdf_attachment)
                    
                    # Send email
                    server.sendmail(sender_email, receiver_email, msg.as_string())
                    success_count += 1
                    status_container.success(f"✅ Sent to {receiver_email}")
                except Exception as e:
                    error_count += 1
                    failed_emails.append((receiver_email, str(e)))
                    status_container.error(f"❌ Failed to send to {receiver_email}: {str(e)}")
                
                # Update progress
                progress = (i + 1) / total
                progress_bar.progress(progress)
                status_text.info(f"**Progress:** {i+1}/{total} emails processed | ✅ {success_count} sent | ❌ {error_count} errors")
            
            # Final status
            progress_bar.empty()
            status_text.empty()
            
            if success_count > 0:
                st.success(f"## ✅ Successfully sent {success_count}/{total} emails!")
            
            # Show failed emails in a dedicated error box
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

# Footer
st.markdown("---")
st.markdown('<div class="footer">Cold Email Sender | Secure Gmail Integration</div>', unsafe_allow_html=True)