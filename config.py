import os

# MySQL configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_NAME = os.getenv("DB_NAME", "ai_study_buddy")

# Hugging Face
HF_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-125M"
HF_TOKEN = os.getenv("HF_TOKEN")  # Set this in .env

# Stripe
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
