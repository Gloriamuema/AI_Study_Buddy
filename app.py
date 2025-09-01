from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json
import re

app = Flask(__name__)
CORS(app)  # Allow frontend access

# ----------------------------
# Hugging Face configuration
# ----------------------------
HF_MODEL = "EleutherAI/gpt-neo-125M"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HF_TOKEN = os.getenv("HF_TOKEN")  # Set your Hugging Face token in environment

if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set!")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# ----------------------------
# Flashcard generation route
# ----------------------------
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
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 250}
        }

        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        print("HF Response Status:", response.status_code)
        raw_output = response.text
        print("HF Raw Output:", raw_output)

        flashcards = []

        # Try to extract JSON array from model output
        try:
            flashcards = json.loads(re.search(r"\[.*\]", raw_output, re.S).group())
        except Exception as e:
            print("JSON parse failed:", e)
            # Fallback dummy flashcards
            flashcards = [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} for i in range(5)]

        # Ensure exactly 5 flashcards
        if len(flashcards) < 5:
            flashcards += [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} 
                           for i in range(5 - len(flashcards))]
        else:
            flashcards = flashcards[:5]

        return jsonify({"flashcards": flashcards})

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        flashcards = [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} for i in range(5)]
        return jsonify({"flashcards": flashcards, "error": str(e)})

    except Exception as e:
        print("Unexpected error:", e)
        flashcards = [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} for i in range(5)]
        return jsonify({"flashcards": flashcards, "error": str(e)})

# ----------------------------
# Run the server
# ----------------------------
if __name__ == "__main__":
    print("Starting Flask server...")
    print("HF_MODEL:", HF_MODEL)
    print("HF_API_URL:", HF_API_URL)
    app.run(debug=True)
