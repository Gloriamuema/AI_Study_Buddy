-- Create the database
CREATE DATABASE IF NOT EXISTS ai_study_buddy;
USE ai_study_buddy;

-- Table for storing user notes
CREATE TABLE IF NOT EXISTS study_notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    notes TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing generated flashcards
CREATE TABLE IF NOT EXISTS flashcards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    note_id INT,                          -- link flashcard to study_notes
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT NULL,      -- track if user answered correctly
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (note_id) REFERENCES study_notes(id) ON DELETE CASCADE
);

-- ✅ Insert sample study notes
INSERT INTO study_notes (notes) VALUES
("The capital of France is Paris. Water boils at 100 degrees Celsius. The largest planet is Jupiter.");

-- ✅ Insert sample flashcards (linked to note_id = 1)
INSERT INTO flashcards (note_id, question, answer) VALUES
(1, "What is the capital of France?", "Paris"),
(1, "At what temperature does water boil (Celsius)?", "100"),
(1, "Which is the largest planet?", "Jupiter");

-- ✅ Query to see flashcards
SELECT f.id, f.question, f.answer, f.is_correct, s.notes
FROM flashcards f
JOIN study_notes s ON f.note_id = s.id;

-- ✅ Query to update user response (marking correct/incorrect)
UPDATE flashcards SET is_correct = TRUE WHERE id = 1;
UPDATE flashcards SET is_correct = FALSE WHERE id = 2;
UPDATE flashcards SET is_correct = TRUE WHERE id = 3;
-- ✅ Query to see updated flashcards with user responses
SELECT * FROM flashcards;
-- ✅ Query to delete a study note and its associated flashcards

