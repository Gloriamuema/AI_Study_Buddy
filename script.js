let stripe = Stripe("pk_test_your_stripe_publishable_key"); // Replace with your Stripe publishable key

async function signup() {
  const username = document.getElementById("signup-username").value;
  const password = document.getElementById("signup-password").value;

  const res = await fetch("http://localhost:5000/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  alert(data.message || data.error);
}

async function login() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  const res = await fetch("http://localhost:5000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  if (data.message) {
    alert(data.message);
    document.getElementById("auth").style.display = "none";
    document.getElementById("flashcards-section").style.display = "block";
  } else {
    alert(data.error);
  }
}

async function generateFlashcards() {
  const topic = document.getElementById("topic").value;
  const res = await fetch("http://localhost:5000/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ topic })
  });

  const data = await res.json();
  const container = document.getElementById("flashcards");
  container.innerHTML = "";
  data.flashcards.forEach(fc => {
    const div = document.createElement("div");
    div.innerHTML = `<strong>Q:</strong> ${fc.question} <br> <strong>A:</strong> ${fc.answer}<hr>`;
    container.appendChild(div);
  });
}

async function checkout() {
  const res = await fetch("http://localhost:5000/create-checkout-session", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include"
  });

  const data = await res.json();
  if (data.id) {
    stripe.redirectToCheckout({ sessionId: data.id });
  } else {
    alert(data.error);
  }
}
