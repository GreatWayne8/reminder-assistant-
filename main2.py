import streamlit as st
import schedule
import time
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import pywhatkit as kit
import pymysql

# Function to connect to the database and retrieve phone numbers
def get_phone_numbers():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='mysql',
        database='amigos',
    )
    cursor = conn.cursor()
    cursor.execute("SELECT number FROM AMS")
    numbers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return numbers


# Function to perform check-in in ERP
def check_in_to_erp(employee_id):
    try:
        # Connect to the ERP database
        connection = connect_to_erp_database()

        # Check if the connection was successful
        if connection is None:
            raise ConnectionError("Unable to connect to ERP database.")

        # Execute the check-in query
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET checked_in = True WHERE user_id = {employee_id};")
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

# error handling
        return True
    except ConnectionError as ce:
        print(f"ConnectionError: {ce}")
        return False
    except Exception as e:
        print(f"Error occurred while checking in to ERP: {e}")
        return False


# def get_phone_numbers():
#     return ["+254701728763"] 

# def get_emails():
#     return ['thegreatesteverart@gmail.com']
    

# Function to connect to the database and retrieve email addresses
def get_emails():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='mysql',
        database='amigos',
    )
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, email FROM AMS")  
    recipients = cursor.fetchall()
    conn.close()
    return recipients


# Function to send email notification
def send_email_notification(subject, body, recipient_email):
    sender_email = "wayne@nathandigital.com"
    sender_password = "Quk04296"

    for recipient in recipient_email:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            st.write(f"Email notification sent successfully to {recipient}.")
            server.quit()
        except Exception as e:
            st.error(f"Error sending email notification to {recipient}: {str(e)}")


# sending SMS notification Function
def send_sms_notification(message, phone_number):
    account_sid = 'AC5fe6d8ce6d37d9fc330b521a552338e4'
    auth_token = 'd6e66eb529512a1e2405e25d5973a8a5'
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body = message,
            from_= '+14159939893',
            to = phone_number
        )
        st.write("SMS notification sent successfully.")
    except Exception as e:
        st.error("Error sending SMS notification: {}".format(str(e)))

# Function to send WhatsApp notification
def send_whatsapp_notification():
    # phone_number = '+254701728763'
    try:
        # kit.sendwhatmsg_to_group("Nathan Digital Kenyan team", "Hey All!", 0, 0)
        kit.sendwhatmsg("+254701728763", "Hi", 0, 0)
        st.write("WhatsApp notification sent successfully.")
    except Exception as e:
        st.error("Error sending WhatsApp notification: {}".format(str(e)))
    
# Function to handle leave notifications
def send_leave_notification(employee_name, leave_date, group_members):
    message = f"{employee_name} will be on leave on {leave_date}."
    for member in group_members:
        send_notification("Email", None, [member.email], None)  
        st.info(f"{message} Notification sent to {member.name}.")      

# Function to send notification basead on the chosen method
def send_notification(notification_method, recipient_name, recipient_email, recipient_phone):
    prompt_message = random.choice(text_data)
    message = f"Hello {recipient_name}, {prompt_message}\n\nWould you like me to check in for you?"
    if notification_method == "Email":
        send_email_notification("Check-in Reminder", message, recipient_email)
    elif notification_method == "SMS":
        send_sms_notification(message, recipient_phone)
    elif notification_method == "WhatsApp":
        send_whatsapp_notification(message, recipient_phone)
        
    
    # Show confirmation prompt
    confirmation = st.confirm("Would you like to check in now?")
    if confirmation:
        # Call function to perform check-in
        check_in_to_erp(id)  
        st.success("You have been successfully checked in!")


def connect_to_erp_database():
    try:
        # Establishing a connection to the ERP database
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='mysql',
            database='amigos',
        )
        return conn
    except pymysql.Error as e:
        print(f"Error connecting to ERP database: {e}")
        return None
("Notifications sent successfully!")



def run_scheduler():
    st.title("CHECK-IN REMINDER")
    if st.button("Send Notification"):
        notification_method = st.selectbox("Choose notification method", ["Email", "SMS", "WhatsApp"])
        if notification_method == "Email":
# Fetching recipients along with their names from the database
            recipients = get_emails()  
            for recipient_name, recipient_email in recipients:
                send_notification(notification_method, recipient_name, [recipient_email], None)
        elif notification_method == "SMS" or notification_method == "WhatsApp":
            phone_numbers = get_phone_numbers()
            for phone_number in phone_numbers:
                send_notification(notification_method, None, None, phone_number)
        st.success("Notifications sent successfully!")
        st.selectbox("do you want me to sign in for you?")
        id = st.text_input("Enter Employee ID:")
        if st.button("Check-in"):
            check_in_to_erp(id)

# Define scheduler task
def schedule_notifications():
    schedule.every(3).seconds.do(run_scheduler)

# Text data for prompts
text_data = [
    "Don't forget to check-in to the ERP portal app at least once a day.",
    "Remember to check-in to the ERP portal system to check for updates.",
    "It's important to check-in regularly to ensure you don't miss any notifications.",
    "Don't neglect logging in to the app, as it provides valuable insights and reminders.",
    "Make sure to log in every morning to start your day with the latest information.",
    "Logging in daily is crucial for staying connected and informed.",
    "Set a reminder to check-in to the AI assistant app daily for the best user experience.",
    "Don't forget to log in and review your tasks and notifications.",
    "Logging in regularly helps personalize your experience with the AI assistant.",
    "Keep in mind to log in frequently to take advantage of all app features.",
]

if __name__ == "__main__":
    run_scheduler()

    # Start scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)
