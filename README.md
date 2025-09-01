# AI_Study_Buddy
Vibe Coding 4-3-2 Hackathon 3.0 repository

# 🧑‍🎓 AI Study Buddy

AI Study Buddy is a Flask-based web application that helps students turn their notes into flashcards, track study progress, and review effectively.  
It uses **Flask + MySQL** on the backend and supports features like user accounts, flashcards, and study sessions.

---

## 🚀 Features
- User registration and login with secure password hashing
- Create study sessions from raw notes
- Auto-generate flashcards (Q&A pairs)
- Track progress with review history
- Simple REST API endpoints for frontend integration

---

## ⚙️ Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai_study_buddy.git
   cd ai_study_buddy
Create a virtual environment & install dependencies

bash
Copy code
python -m venv venv
source venv/bin/activate   # on Mac/Linux
venv\Scripts\activate      # on Windows
pip install -r requirements.txt
Database Setup

Create the database:

sql
Copy code
CREATE DATABASE ai_study_buddy;
Run the table schema (from schema.sql):

users

study_sessions

flashcards

study_progress

Update your db_config in app.py:

python
Copy code
db_config = {
    'user': 'root',
    'password': 'yourpassword',
    'host': '127.0.0.1',
    'database': 'ai_study_buddy'
}
▶️ Running the App
Start the Flask server:

bash
Copy code
python app.py
App will run on: http://127.0.0.1:5000

📂 Project Structure
csharp
Copy code
ai_study_buddy/
│── app.py              # Flask backend
│── schema.sql          # Database schema
│── requirements.txt    # Python dependencies
│── static/             # Frontend assets (if any)
│── templates/          # HTML templates (if using Jinja2)
🔒 Security
Passwords are hashed before storing in DB

Input validation on flashcards & sessions

Use environment variables for database credentials in production

🙌 Contributing
Pull requests are welcome!
For major changes, please open an issue first to discuss what you would like to change.
