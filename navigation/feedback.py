import streamlit as st
import smtplib
from email.message import EmailMessage

# Receiver's email address
RECEIVER_EMAIL = "burakg404@gmail.com"

def send_feedback_email(name, email, feedback_type, feedback_message):
    msg = EmailMessage()
    msg.set_content(f"Feedback from {name}\n\nType: {feedback_type}\n\nMessage:\n{feedback_message}")
    msg["Subject"] = "User Feedback"
    msg["From"] = "your_app@example.com"  # Sender's email address
    msg["To"] = RECEIVER_EMAIL  # Using the receiver_email variable

    try:
        # Connect to the SMTP server and send the email
        smtp_server = smtplib.SMTP("smtp.example.com", 587)  # Replace with your SMTP server details
        smtp_server.starttls()
        smtp_server.login("your_username", "your_password")  # Replace with your SMTP server credentials
        smtp_server.send_message(msg)
        smtp_server.quit()

        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

def pageIV():
    st.subheader("Feedback Form")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email (optional)")
    feedback_type = st.selectbox("Feedback Type", ["Bug Report", "Feature Request", "General Feedback"])
    feedback_message = st.text_area("Feedback Message")
    submit_button = st.button("Submit Feedback")
       
    if submit_button:
        if send_feedback_email(name, email, feedback_type, feedback_message):
            st.success("Thank you for your feedback! An email has been sent.")
        else:
            st.error("There was an error sending your feedback. Please try again later.")

