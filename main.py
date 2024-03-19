import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import pywhatkit as kit
from pymongo import MongoClient
from main_utils import fetch_user_by_email

# Function to establish database connection
def connect_to_database():
    try:
        client = MongoClient("mongodb+srv://app-hr_operation:xAuqDbQ6uvqGo689@nn-hr-operation.5su98.mongodb.net")
        db = client["skeleton-mcs"]
        if db.list_collection_names():
            return db
        else:
            print("No collections found in the database.")
            return None
    except Exception as e:
        print("Could not connect to MongoDB:", e)
        return None


def fetch_recipient_details(method):
    db = connect_to_database()
    recipients = ""
    if db.list_collection_names():
        try:
            collection = db["users"]
            if method == "Email":
                recipients = collection.find({})
            elif method == "SMS":
                recipients = collection.find({"personal.phone": {"$exists": True}})
            elif method == "WhatsApp":
                recipients = collection.find({"personal.whatsapp": {"$exists": True}})
            
            # Extraction of various data
            recipients_data = []
            for recipient in recipients:
                recipients_data.append(recipient)
            return recipients_data
        except Exception as e:
            print("Error fetching recipient details:", e)
    else:
        print("Could not connect to the database.")

# TEST 
def send_email_reminder(email, name):
    smtp_host = "smtp.mailtrap.io"
    smtp_port = 2525
    smtp_username = "1a2d942cf42586"
    smtp_password = "b7e7d769ce74bb"
    email_from = "donotreply@nathanhr.ae"

    message = f"Hi {name},\n\nPlease remember to check in to the system."

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email
    msg['Subject'] = "Check-in Reminder"
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        print(f"Email reminder sent successfully to {email}.")
        server.quit()
    except Exception as e:
        print(f"Error sending email reminder to {email}: {str(e)}")

#  Send SMS reminder function
def send_sms_reminder(phone_number, name):
    account_sid = 'AC5fe6d8ce6d37d9fc330b521a552338e4'
    auth_token = 'd6e66eb529512a1e2405e25d5973a8a5'
    client = Client(account_sid, auth_token)
    
    message = f"Hi {name}, please remember to check in to the system."
    
    try:
        message = client.messages.create(
            body=message,
            from_='+14159939893',
            to=phone_number
        )
        print("SMS reminder sent successfully.")
    except Exception as e:
        print("Error sending SMS reminder: {}".format(str(e)))



#  send WhatsApp reminder Function
def send_whatsapp_reminder(phone_number, name):
    try:
        kit.sendwhatmsg_instantly(phone_number, f"Hi {name}, please remember to check in to the system.")  
        print("WhatsApp reminder sent successfully.")
    except Exception as e:
        print("Error sending WhatsApp reminder: {}".format(str(e)))

def sign_in_user(email, first_name, phone=None, whatsapp=None, sign_in_method=None):
    db = connect_to_database()
    if db is not None: 
        try:
            collection = db["users"]
            user = collection.find_one({"email": email})
            if user:
                # Update user document with first name and contact information
                update_data = {"$set": {"first_name": first_name}}
                if phone:
                    update_data["$set"]["personal.phone"] = phone
                if whatsapp:
                    update_data["$set"]["personal.whatsapp"] = whatsapp
                if sign_in_method:
                    update_data["$set"]["sign_in_method"] = sign_in_method
                collection.update_one({"email": email}, update_data)
                print(f"{first_name}, you are signed in successfully.")
            else:
                print("User not found.")
        except Exception as e:
            print("Error signing in user:", e)
    else:
        print("Failed to connect to the database. Unable to sign in.")


def remind_to_check_in(method):
    recipients = fetch_recipient_details(method)
    if recipients:
        for recipient in recipients:
            if not is_user_on_leave(recipient):
                if method == "Email":
                    send_email_reminder(recipient["email"], recipient["first_name"])
                elif method == "SMS":
                    send_sms_reminder(recipient["personal"]["phone"], recipient["first_name"])
                elif method == "WhatsApp":
                    send_whatsapp_reminder(recipient["personal"]["whatsapp"], recipient["first_name"])



def is_user_on_leave(user):
    # Check if the user has any remaining leave balance or pending leave requests
    leaves = user.get("leaves", {})
    annual_leaves = leaves.get("annual_leaves", 0)
    medical_leaves = leaves.get("medical_leaves", 0)
    unpaid_leaves = leaves.get("unpaid_leaves", 0)
    
    # If leave balance is greater than zero or there are pending leave requests, consider the user as not on leave
    if annual_leaves > 0 or medical_leaves > 0 or unpaid_leaves > 0:
        return False
    
    leaves_approvals = user.get("leaves_approvals", {})
    if leaves_approvals:
        # Check if there are any pending leave requests
        pending_requests = leaves_approvals.get("pending", [])
        if pending_requests:
            return False
        return True



# Function to run_check_in_reminder
def run_check_in_reminder():
    print("How would you like to be reminded to check in?")
    method = input("Choose Email, SMS, or WhatsApp: ").strip().lower()
    if method in ["email", "sms", "whatsapp"]:
        remind_to_check_in(method)
        auto_sign_in = input("Would you like to be signed in automatically? (yes/no): ").strip().lower()
        if auto_sign_in == "yes":
            # Check if contact information is available and sign in automatically
            email = input("Please enter your email: ").strip()
            user = fetch_user_by_email(email)
            if user:
                sign_in_method = method
                if method == "email":
                    sign_in_user(email, user["first_name"], sign_in_method=sign_in_method)
                elif method == "sms" and "personal" in user and "phone" in user["personal"]:
                    sign_in_user(email, user["first_name"], phone=user["personal"]["phone"], sign_in_method=sign_in_method)
                elif method == "whatsapp" and "personal" in user and "whatsapp" in user["personal"]:
                    sign_in_user(email, user["first_name"], whatsapp=user["personal"]["whatsapp"], sign_in_method=sign_in_method)
                else:
                    print(f"No {method} contact information found in your profile.")
            else:
                print("User not found.")
    else:
        print("Invalid method selected.")


if __name__ == "__main__":
    run_check_in_reminder()




