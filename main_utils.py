
import pywhatkit as kit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from pymongo import MongoClient
from bson.objectid import ObjectId

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

def fetch_recipients():
    try:
        db = connect_to_database()
        if db:
            collection = db["users"]
            recipients = collection.find({})
            return list(recipients)
        else:
            return []
    except Exception as e:
        print("Error fetching recipients:", e)
        return []

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

def send_sms_reminder(phone_number, name):
    account_sid = 'your_account_sid'  
    auth_token = 'your_auth_token'  
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


def send_whatsapp_reminder(phone_number, name):
    try:
        kit.sendwhatmsg_instantly(phone_number, f"Hi {name}, please remember to check in to the system.")  
        print("WhatsApp reminder sent successfully.")
    except Exception as e:
        print("Error sending WhatsApp reminder: {}".format(str(e)))


def fetch_user_by_email(email):
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb+srv://app-hr_operation:xAuqDbQ6uvqGo689@nn-hr-operation.5su98.mongodb.net")
        db = client["skeleton-mcs"]
        users_collection = db["users"]
        
        user = users_collection.find_one({"email": email})
        
        client.close()
        return user
    except Exception as e:
        print(f"Error fetching user by email {email}: {e}")
        return None

def sign_in_user(user_id):
    db = connect_to_database()
    if db is not None: 
        try:
            collection = db["users"]
            user = collection.find_one({"_id": ObjectId(user_id)})
            if user:
                # Check if the user is already signed in
                if "first_name" in user:
                    print("User is already signed in.")
                    return True
                
                # If the user is not signed in, proceed with sign-in
                # For automatic sign-in, assume the user is identified without needing to enter email or phone
                first_name = "John"  # Example: Assign a default first name for automatic sign-in
                # Update user document with first name
                collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"first_name": first_name}})
                print(f"{first_name}, you are signed in successfully.")
                return True
            else:
                print("User not found.")
                return False
        except Exception as e:
            print("Error signing in user:", e)
            return False
    else:
        print("Failed to connect to the database. Unable to sign in.")
        return False
