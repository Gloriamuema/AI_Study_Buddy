// script.js

document.getElementById("generate-btn").addEventListener("click", async () => {
    const notes = document.getElementById("study-notes").value;
    const generateBtn = document.getElementById("generate-btn");
    const loader = generateBtn.querySelector(".loader");
    const btnText = generateBtn.querySelector(".btn-text");

    if (!notes.trim()) {
        alert("Please paste your study notes first!");
        return;
    }

    // Show loading state
    btnText.classList.add("hidden");
    loader.classList.remove("hidden");

    try {
        // Send notes to Flask backend
        
        const response = await fetch("http://127.0.0.1:5000/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ notes }),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch flashcards");
        }

        const data = await response.json();
        const flashcards = data.flashcards;

        if (!flashcards || flashcards.length === 0) {
            alert("No flashcards were generated. Try different notes.");
            return;
        }

        // Show flashcards section
        document.getElementById("flashcard-section").classList.remove("hidden");

        let currentIndex = 0;
        const questionText = document.getElementById("question-text");
        const answerText = document.getElementById("answer-text");
        const cardCounter = document.getElementById("card-counter");
        const flashcard = document.getElementById("current-flashcard");

        function updateCard() {
            questionText.textContent = flashcards[currentIndex].question;
            answerText.textContent = flashcards[currentIndex].answer;
            cardCounter.textContent = `${currentIndex + 1} / ${flashcards.length}`;
            flashcard.classList.remove("flipped"); // Reset to question side
        }

        updateCard();

        // Navigation
        document.getElementById("next-btn").onclick = () => {
            if (currentIndex < flashcards.length - 1) {
                currentIndex++;
                updateCard();
            }
        };

        document.getElementById("prev-btn").onclick = () => {
            if (currentIndex > 0) {
                currentIndex--;
                updateCard();
            }
        };

        // Flip card on click
        flashcard.addEventListener("click", () => {
            flashcard.classList.toggle("flipped");
        });

    } catch (err) {
        alert("Error: " + err.message);
    } finally {
        // Reset button state
        loader.classList.add("hidden");
        btnText.classList.remove("hidden");
    }
});
