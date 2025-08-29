# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import requests
import os

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'ai_study_buddy'
}

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HF_TOKEN = "your_huggingface_token"

@app.route('/api/generate-flashcards', methods=['POST'])
def generate_flashcards():
    data = request.json
    notes = data.get('notes')
    
    # Generate flashcards using Hugging Face
    flashcards = generate_with_huggingface(notes)
    
    # Save to database
    session_id = save_study_session(notes, flashcards)
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'flashcards': flashcards
    })

def generate_with_huggingface(text):
    # Call Hugging Face API for question generation
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Process text and generate questions
    questions = []
    sentences = text.split('.')
    
    for i, sentence in enumerate(sentences[:5]):
        if len(sentence.strip()) > 10:
            payload = {
                "inputs": f"Generate a study question for: {sentence}",
                "parameters": {"max_length": 100}
            }
            
            response = requests.post(HF_API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                question = result[0]['generated_text'] if result else f"What is the main concept in: {sentence}?"
                
                questions.append({
                    'id': i + 1,
                    'question': question,
                    'answer': sentence.strip()
                })
    
    return questions

if __name__ == '__main__':
    app.run(debug=True)
