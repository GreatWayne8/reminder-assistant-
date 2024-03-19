from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from main_utils import send_email_reminder, send_sms_reminder, send_whatsapp_reminder, fetch_recipients, sign_in_user

app = Flask(__name__)

@app.route('/api/notification-methods', methods=['GET'])
def get_notification_methods():
    return jsonify({'notification_methods': ['email', 'sms', 'whatsapp']})

def update_notification_method(user_id, selected_method):
    try:
        # Connecting to the database 
        client = MongoClient("mongodb+srv://app-hr_operation:xAuqDbQ6uvqGo689@nn-hr-operation.5su98.mongodb.net/hrdirect-dev")
        db = client["skeleton-mcs"]
        users_collection = db["users"]
        
        # Update user's profile with the selected notification method
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"notification_method": selected_method}}
        )
        
        client.close()
        return True
    except Exception as e:
        
        print(f"Error updating notification method for user {user_id}: {e}")
        return False

# Endpoint to set notification method
@app.route('/api/notification-method', methods=['POST'])
def set_notification_method():
    data = request.json
    selected_method = data.get('method', '').lower()
    user_id = data.get('user_id')

    if selected_method in ['email', 'sms', 'whatsapp']:
        if user_id:
            if update_notification_method(user_id, selected_method):
                return jsonify({'message': f'Notification method set to {selected_method}.'}), 200
            else:
                return jsonify({'error': 'Failed to update notification method.'}), 500
        else:
            return jsonify({'error': 'User ID is required.'}), 400
    else:
        return jsonify({'error': 'Invalid notification method.'}), 400

# Defining a route to trigger reminders
@app.route('/api/reminder', methods=['POST'])
def trigger_reminder():
    data = request.json
    method = data.get('method', '').lower()
    if method in ['email', 'sms', 'whatsapp']:
        # Fetch recipients from the DB
        recipients = fetch_recipients()
        for recipient in recipients:
            if method == 'email':
                send_email_reminder(recipient['email'], recipient['first_name'])
            elif method == 'sms':
                send_sms_reminder(recipient['phone'], recipient['first_name'])
            elif method == 'whatsapp':
                send_whatsapp_reminder(recipient['whatsapp'], recipient['first_name'])
        return jsonify({'message': f'Reminder triggered via {method}.'}), 200
    else:
        return jsonify({'error': 'Invalid method.'}), 400

# Endpoint for automatic sign-in
@app.route('/api/auto-sign-in', methods=['POST'])
def auto_sign_in():
    data = request.json
    user_id = data.get('user_id')
    if user_id:
        sign_in_user(user_id)
        return jsonify({'message': 'User signed in successfully.'}), 200
    else:
        return jsonify({'error': 'User ID is required.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
