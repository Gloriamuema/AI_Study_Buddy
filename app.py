from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import json
import re

app = Flask(__name__)
CORS(app)  # Allow all origins for testing

# Hugging Face model URL
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_TOKEN = os.getenv("HF_TOKEN")  # Make sure this is set in your environment

if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set!")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

@app.route("/generate", methods=["POST"])
def generate_flashcards():
    data = request.get_json()
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    prompt = f"Generate 5 simple flashcards (question and answer) about {topic}. Format them as: question: ..., answer: ..."

    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=30
        )

        # If API fails, fallback to dummy flashcards
        if response.status_code != 200:
            flashcards = [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} for i in range(5)]
            return jsonify({"flashcards": flashcards})

        raw_output = response.json()
        print("HF Raw Output:", raw_output)  # Debugging

        # Attempt to parse generated text
        generated_text = ""
        if isinstance(raw_output, list) and "generated_text" in raw_output[0]:
            generated_text = raw_output[0]["generated_text"]
        else:
            generated_text = str(raw_output)

        # Extract flashcards from text using regex
        flashcards = []
        lines = generated_text.split("\n")
        for line in lines:
            if "question" in line.lower() and "answer" in line.lower():
                # Simple split by "answer:"
                parts = re.split(r"answer[:\-]", line, flags=re.I)
                if len(parts) == 2:
                    question = parts[0].replace("question", "", 1).strip(" :")
                    answer = parts[1].strip()
                    flashcards.append({"question": question, "answer": answer})

        # Ensure exactly 5 flashcards
        if len(flashcards) < 5:
            flashcards += [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} 
                           for i in range(5 - len(flashcards))]
        else:
            flashcards = flashcards[:5]

        return jsonify({"flashcards": flashcards})

    except requests.exceptions.RequestException as e:
        # Network or API error: fallback
        flashcards = [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} for i in range(5)]
        return jsonify({"flashcards": flashcards})

    except Exception as e:
        # Any other error: fallback
        flashcards = [{"question": f"{topic} Q{i+1}", "answer": f"{topic} A{i+1}"} for i in range(5)]
        return jsonify({"flashcards": flashcards})

if __name__ == "__main__":
    app.run(debug=True)
# Run with: python app.py
# Ensure you have the required packages installed:
# pip install flask flask-cors requests
# And set your Hugging Face token in the environment:
# export HF
# Then test with a POST request to /generate with JSON body {"topic": "your_topic"}
