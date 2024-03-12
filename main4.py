import pymysql
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from twilio.rest import Client
import pywhatkit as kit

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
        print(f"Email reminder sent successfully to {email}.")
        server.quit()
    except Exception as e:
        print(f"Error sending email reminder to {email}: {str(e)}")

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
        print("SMS reminder sent successfully.")
    except Exception as e:
        print("Error sending SMS reminder:", str(e))

# Function to send WhatsApp reminder
def send_whatsapp_reminder(phone_number, message):
    try:
        kit.sendwhatmsg(f"{phone_number}", message, 0, 0)
        print("WhatsApp reminder sent successfully.")
    except Exception as e:
        print("Error sending WhatsApp reminder:", str(e))

# Function to remind user to check-in
def remind_to_check_in(method, recipient_email, recipient_phone_number):
    if method == "Email":
        send_email_reminder(recipient_email, "Please remember to check in to the system.")
    elif method == "SMS":
        send_sms_reminder(recipient_phone_number, "Please remember to check in to the system.")
    elif method == "WhatsApp":
        send_whatsapp_reminder(recipient_phone_number, "Please remember to check in to the system.")

# Function to sign user in automatically
def sign_in_user(user_id):
    # Placeholder for sign-in logic
    pass

# Example usage
recipient_email = "muzame60@.com"
recipient_phone_number = "+254701728763"
method = "Email"
remind_to_check_in(method, recipient_email, recipient_phone_number)
user_id = "123456"
sign_in_user(user_id)
