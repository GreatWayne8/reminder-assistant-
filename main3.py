import streamlit as st
import pymysql
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from twilio.rest import Client
import pywhatkit as kit

# Function to connect to the database
def connect_to_database():
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='mysql',
            database='amigos',
        )
        return conn
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to send email reminder
def send_email_reminder(email, message):
    sender_email = "wayne@nathandigital.com" 
    sender_password = "Quk04296"  

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Check-in Reminder"
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        st.write(f"Email reminder sent successfully to {email}.")
        server.quit()
    except Exception as e:
        st.error(f"Error sending email reminder to {email}: {str(e)}")

# Function to send SMS reminder
def send_sms_reminder(phone_number, message):
    account_sid = 'AC5fe6d8ce6d37d9fc330b521a552338e4'
    auth_token = 'd6e66eb529512a1e2405e25d5973a8a5'
    client = Client(account_sid, auth_token)
    
    try:
        message = client.messages.create(
            body=message,
            from_='+14159939893',
            to=phone_number
        )
        st.write("SMS reminder sent successfully.")
    except Exception as e:
        st.error("Error sending SMS reminder: {}".format(str(e)))

# Function to send WhatsApp reminder
def send_whatsapp_reminder(phone_number, message):
    try:
        kit.sendwhatmsg(phone_number, message, 0, 0)
        st.write("WhatsApp reminder sent successfully.")
    except Exception as e:
        st.error("Error sending WhatsApp reminder: {}".format(str(e)))

# Function to prompt user for preferred reminder method
def prompt_reminder_method():
    return st.selectbox("How would you like to receive the reminder for check-in?", ["Email", "SMS", "WhatsApp"])

# Function to remind user to check-in
def remind_to_check_in(method, recipient):
    if method == "Email":
        send_email_reminder(recipient['email'], "Please remember to check in to the system. Would you like to automatically check in?")
    elif method == "SMS":
        send_sms_reminder(recipient['phone_number'], "Please remember to check in to the system. Would you like to automatically check in?")
    elif method == "WhatsApp":
        send_whatsapp_reminder(recipient['phone_number'], "Please remember to check in to the system. Would you like to automatically check in?")

    st.success("Reminder sent successfully!")

# Function to prompt user for automatic check-in
def prompt_auto_check_in():
    return st.checkbox("Automatically check me in")

# Function to sign user in automatically
def sign_in_user(user_id):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET checked_in = 1 WHERE id = {user_id};")
            conn.commit()
            st.success("You have been successfully checked in!")
        except pymysql.Error as e:
            st.error(f"Error updating check-in status: {e}")
        finally:
            conn.close()
    else:
        st.error("Could not connect to the database.")

# Function to run the check-in reminder
def run_check_in_reminder():
    st.title("Check-in Reminder")

    # Prompt user for preferred reminder method
    method = prompt_reminder_method()

    if st.button("Send Reminder"):
        # Replace this with fetching recipient details from the database
        recipient = {'email': 'recipient@example.com', 'phone_number': '+1234567890', 'id': 1}
        remind_to_check_in(method, recipient)

    if method:
        auto_check_in = prompt_auto_check_in()
        if auto_check_in and st.button("Check-in Automatically"):
            user_id = st.text_input("Enter your user ID:")
            if user_id:
                sign_in_user(user_id)

# Main function to run the Streamlit app
def main():
    run_check_in_reminder()

if __name__ == "__main__":
    main()
