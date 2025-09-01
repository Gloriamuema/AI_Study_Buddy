// script.js

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("flashcard-form");
  const topicInput = document.getElementById("topic");
  const flashcardsContainer = document.getElementById("flashcards");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const topic = topicInput.value.trim();
    if (!topic) return;

    flashcardsContainer.innerHTML = "<p>Generating flashcards...</p>";

    try {
      const response = await fetch("http://127.0.0.1:5000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ topic })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      const flashcards = data.flashcards || [];

      flashcardsContainer.innerHTML = ""; // Clear previous cards

      flashcards.forEach(card => {
        const cardDiv = document.createElement("div");
        cardDiv.className = "flashcard";

        cardDiv.innerHTML = `
          <div class="front"><strong>Q:</strong> ${card.question}</div>
          <div class="back"><strong>A:</strong> ${card.answer}</div>
        `;

        // Add simple flip effect
        cardDiv.addEventListener("click", () => {
          cardDiv.classList.toggle("flipped");
        });

        flashcardsContainer.appendChild(cardDiv);
      });

    } catch (err) {
      console.error("Error fetching flashcards:", err);
      flashcardsContainer.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
    }
  });
});
