# app.py
from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import torch # This import is sometimes necessary

# Initialize the Flask app
app = Flask(__name__)

# Load the Zero-Shot Classification model once when the app starts
# This is more efficient than loading it for every request
print("Loading Hugging Face model...")
# Using a smaller model that is optimized for performance and lower memory usage
classifier = pipeline("zero-shot-classification", 
                        model="valhalla/distilbart-mnli-12-3")
print("Model loaded successfully.")

# Route to serve the main HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the classification
@app.route('/classify', methods=['POST'])
def classify_message():
    # Get the JSON data sent from the frontend
    data = request.get_json()
    sms_message = data.get('sms_text', '')

    if not sms_message:
        return jsonify({'error': 'No text provided'}), 400

    # These are the categories the model will choose from
    candidate_labels = [
        'E-Commerce', 
        'Banking/Finance', 
        'Promotions',
        'Entertainment', 
        'Education', 
        'Travel',
        'Healthcare',
        'Social',
        'Utility'
    ]

    # Perform the classification
    result = classifier(sms_message, candidate_labels)
    
    # Return the result as JSON
    return jsonify(result)

# Run the app
if __name__ == '__main__':
    # Use port 8080 to avoid potential conflicts
    app.run(host='0.0.0.0', port=8080, debug=True)