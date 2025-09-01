document.getElementById("flashcard-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const topic = document.getElementById("topic").value;
    const responseDiv = document.getElementById("flashcards");
    responseDiv.innerHTML = "<p>Generating flashcards...</p>";

    try {
        const response = await fetch("http://127.0.0.1:5000/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic: topic })
        });

        if (!response.ok) {
            throw new Error("Failed to fetch flashcards from server.");
        }

        const data = await response.json();

        // Check if we actually got flashcards
        if (!Array.isArray(data) || data.length === 0) {
            responseDiv.innerHTML = "<p>No flashcards generated.</p>";
            return;
        }

        // Render flashcards
        responseDiv.innerHTML = "";
        data.forEach((card, index) => {
            const cardDiv = document.createElement("div");
            cardDiv.classList.add("flashcard");
            cardDiv.innerHTML = `
                <p><strong>Q${index + 1}:</strong> ${card.question}</p>
                <p><em>Answer:</em> ${card.answer}</p>
            `;
            responseDiv.appendChild(cardDiv);
        });

    } catch (error) {
        console.error("Error:", error);
        responseDiv.innerHTML = "<p>Error generating flashcards. Please try again.</p>";
    }
});
