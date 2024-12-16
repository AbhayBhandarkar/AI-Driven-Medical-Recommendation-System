from flask import Flask, request, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
from transformers import pipeline
from PIL import Image
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY")

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['hospital_recommender']  # Database name
users_collection = db['users']  # Users collection

logging.basicConfig(level=logging.INFO)
logging.info("Connected to MongoDB")


# Load Deep Learning Models
tumor_pipe = pipeline("image-classification", model="Devarshi/Brain_Tumor_Classification")
disease_pipe = pipeline("text-classification", model="rppadmakumar/Disease_Prediction")


@app.route('/register', methods=['POST'])
def register():
    """User registration endpoint."""
    try:
        data = request.json
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'status': 'failure', 'message': 'Invalid input'}), 400

        # Check if the username already exists
        if users_collection.find_one({'username': data['username']}):
            return jsonify({'status': 'failure', 'message': 'Username already exists'}), 400

        # Hash the password and store the user
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        users_collection.insert_one({'username': data['username'], 'password': hashed_password})
        return jsonify({'status': 'success'})
    except Exception as e:
        logging.error(f"Error during registration: {e}")
        return jsonify({'status': 'failure', 'message': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    """User login endpoint."""
    try:
        data = request.json
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'status': 'failure', 'message': 'Invalid input'}), 400

        # Find the user
        user = users_collection.find_one({'username': data['username']})
        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
            session['username'] = data['username']
            return jsonify({'status': 'success'})
        return jsonify({'status': 'failure', 'message': 'Invalid credentials'}), 401
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({'status': 'failure', 'message': str(e)}), 500


@app.route('/upload-mri', methods=['POST'])
def upload_mri():
    """Endpoint to upload and classify MRI images."""
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'failure', 'message': 'No file uploaded'}), 400

        image_file = request.files['file']
        if not image_file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            return jsonify({'status': 'failure', 'message': 'Invalid file format'}), 400

        # Save and process the image
        image_path = "uploaded_image.jpg"
        image_file.save(image_path)

        predictions = tumor_pipe(image_path)
        os.remove(image_path)  # Cleanup
        return jsonify(predictions[0])  # Return the top prediction
    except Exception as e:
        logging.error(f"Error during MRI upload: {e}")
        return jsonify({'status': 'failure', 'message': str(e)}), 500


@app.route('/diagnose', methods=['POST'])
def diagnose():
    """Endpoint to predict diseases based on symptoms."""
    try:
        symptoms = request.json.get('symptoms')
        if not symptoms:
            return jsonify({'status': 'failure', 'message': 'Symptoms not provided'}), 400

        predictions = disease_pipe(symptoms)
        return jsonify(predictions[0])  # Return the top prediction
    except Exception as e:
        logging.error(f"Error during diagnosis: {e}")
        return jsonify({'status': 'failure', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
