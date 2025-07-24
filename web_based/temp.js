await fetch("http://localhost:8000/ask", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ question: "What is Article 21?" })
});
