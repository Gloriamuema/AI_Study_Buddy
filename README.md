AI_Study_Buddy
Vibe Coding 4-3-2 Hackathon 3.0 repository

 AI Study Buddy

AI Study Buddy is a Flask-based web application that helps students turn their notes into flashcards, track study progress, and review effectively.  
It uses **Flask + MySQL** on the backend and supports features like user accounts, flashcards, and study sessions.


Main Flask app 
Database models
Python dependencies
Config (DB, Hugging Face, Stripe keys)
CSS for frontend
JS for frontend

 Features
- User registration and login with secure password hashing
- Create study sessions from raw notes
- Auto-generate flashcards (Q&A pairs)
- Track progress with review history
- Simple REST API endpoints for frontend integration

Setup

  Clone the repository
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

Running the App
Start the Flask server:

bash
Copy code
python app.py
App will run on: http://127.0.0.1:5000

Deployment link
https://gloriamuema.github.io/AI_Study_Buddy/

Passwords are hashed before storing in DB

Input validation on flashcards & sessions

Use environment variables for database credentials in production

Contributing
Pull requests are welcome!

