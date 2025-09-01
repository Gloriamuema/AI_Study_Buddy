from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

app = Flask(__name__)
CORS(app)

# Get Hugging Face token from environment variable
#setting up environment variable in terminal: set HF_TOKEN=your_token_here
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"  # lightweight model for testing
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

@app.route("/api/generate", methods=["POST"])
def generate_flashcards():
    try:
        data = request.get_json()
        topic = data.get("topic", "general knowledge")

        prompt = f"Generate 3 flashcards on the topic '{topic}'. Format as Q: question, A: answer."

        response = requests.post(
            HF_API_URL,
            headers=headers,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 150, "temperature": 0.8}},
        )

        if response.status_code != 200:
            return jsonify({"error": f"Hugging Face API error: {response.text}"}), 500

        generated_text = response.json()[0]["generated_text"]

        # Split into flashcards
        flashcards = []
        for line in generated_text.split("\n"):
            if "Q:" in line or "A:" in line:
                flashcards.append(line.strip())

        return jsonify({"flashcards": flashcards})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)












