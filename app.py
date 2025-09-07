# app.py (Production Ready)
from flask import Flask, request, jsonify, render_template
from transformers import pipeline

# Initialize the Flask app
app = Flask(__name__)

# Load the model once when the app starts
print("Loading Hugging Face model...")
# Using MobileBERT, a model specifically designed for low-resource environments.
classifier = pipeline("zero-shot-classification", 
                        model="typeform/mobilebert-uncased-mnli")
print("Model loaded successfully.")

# Route to serve the main HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the classification
@app.route('/classify', methods=['POST'])
def classify_message():
    data = request.get_json()
    sms_message = data.get('sms_text', '')

    if not sms_message:
        return jsonify({'error': 'No text provided'}), 400

    candidate_labels = [
        'E-Commerce', 'Banking/Finance', 'Promotions', 'Entertainment', 
        'Education', 'Travel', 'Healthcare', 'Social', 'Utility'
    ]

    result = classifier(sms_message, candidate_labels)
    return jsonify(result)

# The app.run() block has been removed. Gunicorn will run this file.