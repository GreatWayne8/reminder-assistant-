import nltk
import re
import schedule
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Download NLTK resources
nltk.download("punkt")
nltk.download("stopwords")

# Define function to preprocess text
def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in stopwords.words("english")]
    return " ".join(tokens)

# Sample usage of text preprocessing
sample_text = "Don't forget to log in to the assistant AI app."
preprocessed_text = preprocess_text(sample_text)
print(preprocessed_text)

# Text data for training
text_data = [
    "Don't forget to log in to the ERP portal app at in a day.",
    "Remember to log in to the ERP portal system to check for updates.",
    "It's important to log in regularly to ensure you don't miss any notifications.",
    "Don't neglect logging in to the app, as it provides valuable insights and reminders.",
    "Make sure to log in every morning to start your day with the latest information.",
    "Logging in daily is crucial for staying connected and informed.",
    "Set a reminder to log in to the ERP app daily for the best user experience.",
    "Don't forget to log in and review your tasks and notifications.",
    "Logging in regularly helps personalize your experience with the ERP portal.",
    "Keep in mind to log in frequently to take advantage of all app features.",
]

# Vectorize text data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform([preprocess_text(text) for text in text_data])

# Labelling the data as either "log_in" or "not_log_in"
y = ["log_in" if "log in" in text else "not_log_in" for text in text_data]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='weighted'))
print("Recall:", recall_score(y_test, y_pred, average='weighted'))
print("F1-score:", f1_score(y_test, y_pred, average='weighted'))

# Function to prompt the user to log in
def prompt_to_log_in():
    print("Prompting to log in now!")

# Schedule the prompt after 1 minute from now (for testing)
schedule.every(1).minutes.do(prompt_to_log_in)

# Main loop to run scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
