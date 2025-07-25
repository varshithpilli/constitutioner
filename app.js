document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const chatMessages = document.getElementById('chatMessages');
  const chatMain = document.querySelector('.chat-main');
  const sendBtn = chatForm.querySelector('button[type="submit"], .chat-send-btn');

  let isProcessing = false;

  function setInputEnabled(enabled) {
    if (sendBtn) sendBtn.disabled = !enabled;
    if (!enabled) {
      chatInput.placeholder = 'Send disabled...';
    } else {
      chatInput.placeholder = 'Type your query...';
    }
  }

  function appendMessage(text, sender = 'user') {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${sender}`;
    msgDiv.textContent = text;
    let copyBtn = null;
    if (sender === 'bot') {
      msgDiv.textContent = '';
      const span = document.createElement('span');
      span.textContent = text;
      span.className = 'bot-text';
      msgDiv.appendChild(span);
      // Create copy button as a sibling below
      copyBtn = document.createElement('button');
      copyBtn.className = 'copy-btn-below';
      copyBtn.textContent = '📋';
      copyBtn.onclick = async () => {
        try {
          await navigator.clipboard.writeText(text);
          copyBtn.textContent = '✅';
          setTimeout(() => { copyBtn.textContent = '📋'; }, 1200);
        } catch {
          copyBtn.textContent = '⚠️';
          setTimeout(() => { copyBtn.textContent = '📋'; }, 1200);
        }
      };
    }
    chatMessages.appendChild(msgDiv);
    if (copyBtn) chatMessages.appendChild(copyBtn);
    return msgDiv;
  }

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (isProcessing) return;
    const userMsg = chatInput.value.trim();
    if (!userMsg) return;
    isProcessing = true;
    setInputEnabled(false);
    appendMessage(userMsg, 'user');
    chatInput.value = '';
    const typingMsg = appendMessage('Typing...', 'bot');
    try {
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userMsg })
      });
      if (!response.ok) throw new Error('API error');
      const data = await response.json();
      typingMsg.querySelector('.bot-text').textContent = data.answer || '[No answer returned]';
      // Update the copy button to copy the new answer
      const nextBtn = typingMsg.nextElementSibling;
      if (nextBtn && nextBtn.classList.contains('copy-btn-below')) {
        nextBtn.onclick = async () => {
          try {
            await navigator.clipboard.writeText(data.answer || '[No answer returned]');
            nextBtn.textContent = '✅';
            setTimeout(() => { nextBtn.textContent = '📋'; }, 1200);
          } catch {
            nextBtn.textContent = '⚠️';
            setTimeout(() => { nextBtn.textContent = '📋'; }, 1200);
          }
        };
      }
    } catch (err) {
      typingMsg.querySelector('.bot-text').textContent = 'Sorry, there was an error getting a response.';
      const nextBtn = typingMsg.nextElementSibling;
      if (nextBtn && nextBtn.classList.contains('copy-btn-below')) {
        nextBtn.onclick = async () => {
          try {
            await navigator.clipboard.writeText('Sorry, there was an error getting a response.');
            nextBtn.textContent = '✅';
            setTimeout(() => { nextBtn.textContent = '📋'; }, 1200);
          } catch {
            nextBtn.textContent = '⚠️';
            setTimeout(() => { nextBtn.textContent = '📋'; }, 1200);
          }
        };
      }
    } finally {
      isProcessing = false;
      setInputEnabled(true);
      chatInput.focus();
    }
  });
});
