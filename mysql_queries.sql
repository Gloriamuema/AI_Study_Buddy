-- Create database
CREATE DATABASE ai_study_buddy;
USE ai_study_buddy;

-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Study sessions table
CREATE TABLE study_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    title VARCHAR(255) NOT NULL,
    original_notes TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Flashcards table
CREATE TABLE flashcards (
    id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    difficulty_level INT DEFAULT 1,
    times_reviewed INT DEFAULT 0,
    times_correct INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES study_sessions(id)
);

-- Study progress table
CREATE TABLE study_progress (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    flashcard_id INT,
    is_correct BOOLEAN,
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (flashcard_id) REFERENCES flashcards(id)
);
-- Feedback table
CREATE TABLE feedback (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    session_id INT,
    comments TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (session_id) REFERENCES study_sessions(id)
);
-- Indexes for performance optimization
CREATE INDEX idx_user_id ON study_sessions(user_id);
CREATE INDEX idx_session_id ON flashcards(session_id);
CREATE INDEX idx_flashcard_id ON study_progress(flashcard_id);
CREATE INDEX idx_user_feedback ON feedback(user_id);
CREATE INDEX idx_session_feedback ON feedback(session_id);

