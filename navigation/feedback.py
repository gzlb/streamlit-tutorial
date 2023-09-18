import smtplib
from email.message import EmailMessage

import streamlit as st

# Receiver's email address
RECEIVER_EMAIL = "gzlb358@gmail.com"


def send_feedback_email(name, email, feedback_type, feedback_message):
    msg = EmailMessage()
    msg.set_content(
        f"Feedback from {name}\n\nType: {feedback_type}\n\nMessage:\n{feedback_message}"
    )
    msg["Subject"] = "User Feedback"
    msg["From"] = "youremail@gmail.com"  # Sender's email address
    msg["To"] = RECEIVER_EMAIL

    try:
        # Connect to the SMTP server and send the email
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(
            "gzlb358@gmail.com", "edrreehwnxjeltiu"
        )  # Use your App Password here
        smtp_server.send_message(msg)
        smtp_server.quit()

        return True
    except Exception as e:
        print("Error sending email:", e)
        return False


def pageIV():
    """
    Streamlit app page for collecting and sending user feedback.
    """
    st.subheader("Feedback Form")

    name = st.text_input("Your Name")
    email = st.text_input("Your Email (optional)")
    feedback_type = st.selectbox(
        "Feedback Type",
        ["Bug Report", "Feature Request", "General Feedback"],
    )
    feedback_message = st.text_area("Feedback Message")
    submit_button = st.button("Submit Feedback")

    if submit_button:
        if send_feedback_email(name, email, feedback_type, feedback_message):
            st.success("Thank you for your feedback! An email has been sent.")
        else:
            st.error(
                "There was an error sending your feedback. Please try again later."
            )
