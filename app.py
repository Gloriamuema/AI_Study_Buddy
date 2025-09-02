from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import mysql.connector
import os
import requests
import json
import re
import stripe

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# ----------------------
# Environment Variables
# ----------------------
HF_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-125M"
HF_TOKEN = os.getenv("HF_TOKEN")  # Hugging Face token
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")  # Stripe secret key
stripe.api_key = STRIPE_API_KEY

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not set in environment!")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# ----------------------
# MySQL Configuration
# ----------------------
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "1234"),
    database=os.getenv("DB_NAME", "ai_study_buddy")
)
cursor = db.cursor(dictionary=True)

# ----------------------
# User Authentication
# ----------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username").strip()
    password = data.get("password").strip()

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        db.commit()
        return jsonify({"message": "User registered successfully"})
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username").strip()
    password = data.get("password").strip()

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# ----------------------
# Flashcard Generation (Accessible to all users)
# ----------------------
@app.route("/generate", methods=["POST"])
def generate_flashcards():
    data = request.get_json()
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    prompt = f"""
    Generate 5 concise flashcards about {topic}.
    Format your output as JSON like:
    [
        {{"question": "question1", "answer": "answer1"}},
        {{"question": "question2", "answer": "answer2"}},
        ...
    ]
    """
    try:
        payload = {"inputs": prompt}
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            flashcards = [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} for i in range(5)]
            return jsonify({"flashcards": flashcards, "error": f"Hugging Face error: {response.text}"})

        raw_output = response.json()
        generated_text = raw_output[0].get("generated_text", str(raw_output))

        try:
            flashcards = json.loads(re.search(r"\[.*\]", generated_text, re.S).group())
        except Exception:
            flashcards = [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} for i in range(5)]

        if len(flashcards) < 5:
            flashcards += [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} for i in range(5 - len(flashcards))]
        else:
            flashcards = flashcards[:5]

        return jsonify({"flashcards": flashcards})

    except requests.exceptions.RequestException as e:
        flashcards = [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} for i in range(5)]
        return jsonify({"flashcards": flashcards, "error": str(e)})

# ----------------------
# Stripe Payment
# ----------------------
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = request.get_json()
    amount = data.get("amount", 500)  # $5 default
    currency = data.get("currency", "usd")
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": currency,
                    "product_data": {"name": "AI Study Buddy Premium"},
                    "unit_amount": amount,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=data.get("success_url", "http://localhost:5000/success"),
            cancel_url=data.get("cancel_url", "http://localhost:5000/cancel"),
        )
        return jsonify({"id": session.id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------
# Run Server
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
