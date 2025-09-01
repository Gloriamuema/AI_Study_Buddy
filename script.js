document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("flashcard-form");
  const topicInput = document.getElementById("topic");
  const flashcardsDiv = document.getElementById("flashcards");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const topic = topicInput.value.trim();
    if (!topic) return;

    flashcardsDiv.innerHTML = "<p>Generating flashcards...</p>";

    try {
      const response = await fetch("http://127.0.0.1:5000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic }),
      });

      const data = await response.json();

      if (data.error) {
        flashcardsDiv.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
        return;
      }

      const cards = data.flashcards || [];
      flashcardsDiv.innerHTML = "";

      cards.forEach((card) => {
        const cardDiv = document.createElement("div");
        cardDiv.className = "flashcard";
        cardDiv.innerHTML = `
          <p><strong>Q:</strong> ${card.question}</p>
          <p><strong>A:</strong> ${card.answer}</p>
        `;
        flashcardsDiv.appendChild(cardDiv);
      });

    } catch (err) {
      flashcardsDiv.innerHTML = `<p style="color:red;">Network error: ${err}</p>`;
    }
  });
});
