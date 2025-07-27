document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const chatMessages = document.getElementById("chatMessages");
  const chatMain = document.querySelector(".chat-main");
  const sendBtn = chatForm.querySelector(
    'button[type="submit"], .chat-send-btn'
  );

  let isProcessing = false;

  function setInputEnabled(enabled) {
    if (sendBtn) sendBtn.disabled = !enabled;
    if (!enabled) {
      chatInput.placeholder = "Send disabled...";
    } else {
      chatInput.placeholder = "Type your query...";
    }
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function appendMessage(text, sender = "user") {
    const msgDiv = document.createElement("div");
    msgDiv.className = `chat-message ${sender}`;
    msgDiv.textContent = text;
    let nextBtn = null;
    if (sender === "bot") {
      msgDiv.textContent = "";
      const span = document.createElement("span");
      span.textContent = text;
      span.className = "bot-text";
      msgDiv.appendChild(span);
      // Create copy button as a sibling below
      nextBtn = document.createElement("button");
      nextBtn.className = "copy-btn-below";
      nextBtn.textContent = "📋";
      nextBtn.onclick = async () => {
        try {
          await navigator.clipboard.writeText(text);
          nextBtn.textContent = "✅";
          setTimeout(() => {
            nextBtn.textContent = "📋";
          }, 1200);
        } catch {
          nextBtn.textContent = "⚠️";
          setTimeout(() => {
            nextBtn.textContent = "📋";
          }, 1200);
        }
      };
    }
    chatMessages.appendChild(msgDiv);
    if (nextBtn) chatMessages.appendChild(nextBtn);
    scrollToBottom();
    return msgDiv;
  }

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (isProcessing) return;
    const userMsg = chatInput.value.trim();
    if (!userMsg) return;
    isProcessing = true;
    setInputEnabled(false);
    appendMessage(userMsg, "user");
    chatInput.value = "";
    const typingMsg = appendMessage("Typing...", "bot");
    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMsg }),
      });
      if (!response.ok) throw new Error("API error");

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let done = false;
      let answer = "";

      typingMsg.querySelector(".bot-text").textContent = "";

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          answer += chunk;
          const newHTML = DOMPurify.sanitize(marked.parse(answer));
          typingMsg.querySelector(".bot-text").innerHTML = newHTML;

          scrollToBottom();
        }
      }

      const nextBtn = typingMsg.nextElementSibling;
      if (nextBtn && nextBtn.classList.contains("copy-btn-below")) {
        nextBtn.onclick = async () => {
          try {
            const textToCopy = typingMsg.querySelector(".bot-text").innerText;
            await navigator.clipboard.writeText(textToCopy);
            nextBtn.textContent = "✅";
            setTimeout(() => {
              nextBtn.textContent = "📋";
            }, 1200);
          } catch {
            nextBtn.textContent = "⚠️";
            setTimeout(() => {
              nextBtn.textContent = "📋";
            }, 1200);
          }
        };
      }
      scrollToBottom();
    } catch (err) {
      typingMsg.querySelector(
        ".bot-text"
      ).textContent = `Sorry, there was an error getting a response.`;
      const nextBtn = typingMsg.nextElementSibling;
      if (nextBtn && nextBtn.classList.contains("copy-btn-below")) {
        nextBtn.onclick = async () => {
          try {
            const textToCopy = typingMsg.querySelector(".bot-text").innerText;
            await navigator.clipboard.writeText(textToCopy);
            nextBtn.textContent = "✅";
            setTimeout(() => {
              nextBtn.textContent = "📋";
            }, 1200);
          } catch {
            nextBtn.textContent = "⚠️";
            setTimeout(() => {
              nextBtn.textContent = "📋";
            }, 1200);
          }
        };
      }
      scrollToBottom();
    } finally {
      isProcessing = false;
      setInputEnabled(true);
      chatInput.focus();
    }
  });
});
