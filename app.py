import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend (index.html) to talk to backend

@app.route("/api/generate", methods=["POST"])
def generate_flashcards():
    data = request.get_json()
    topic = data.get("topic", "General")

    # Mock flashcards (replace later with Hugging Face call)
    flashcards = [
        {"question": f"What is {topic}?", "answer": f"{topic} is a key concept to understand."},
        {"question": f"Why is {topic} important?", "answer": f"It helps build a strong foundation in {topic}."},
        {"question": f"Give an example of {topic}.", "answer": f"An example of {topic} is ..."}
    ]

    return jsonify(flashcards)

if __name__ == "__main__":
    app.run(debug=True)
