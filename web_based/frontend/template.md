Here’s a clean, developer-ready **`README.md`**-style document that clearly explains the expected frontend design, behavior, and structure for your project:

---

````markdown
# 💬 AI Chat Frontend — Vite + React + shadcn + Tailwind

This project implements a **dark-themed, anonymous chat interface** that connects to a backend AI model through a **streaming response API**.  
It is built with **Vite + React + shadcn + TailwindCSS**, designed to be simple, responsive, and minimal.

---

## 🧱 Tech Stack

- **Frontend Framework:** Vite + React  
- **Styling:** TailwindCSS (dark mode only)  
- **UI Components:** shadcn/ui  
- **Animations:** motion/react (optional for typing animation)  
- **Markdown Rendering:** react-markdown + remark-gfm  
- **Clipboard Copy:** Built-in Web Clipboard API  
- **Streaming:** `fetch()` + `ReadableStream` from backend endpoint  

---

## 🎯 Functional Requirements

### 1. Overall Layout
- The site **always uses dark mode** — no light theme toggle.  
- The main chat interface is **centered** both vertically and horizontally.  
- The container occupies **75% of the viewport width** and **full height**.  
- The background is a uniform dark color (e.g., `bg-zinc-950`).  
- A simple **header bar** at the top displays the title:  
  > `AI Chat Interface`

---

### 2. Chat Interface Structure

#### Main Components
- **ChatContainer** — holds the scrollable list of messages  
- **ChatInput** — input area at the bottom with:
  - A typing box (`input` or `textarea`)
  - A “Send” button
- **MessageBubble** — displays messages for user and AI

#### Behavior
- **User messages** appear on the **right** side (aligned `self-end`).
- **AI messages** appear on the **left** side (aligned `self-start`).
- Messages are displayed in **chat bubbles** with rounded corners.
- **Streaming responses** are rendered live as the backend sends chunks.
- Markdown inside AI responses is rendered **inline and progressively**.
- Each message bubble (user + AI) includes a small **copy button** in the top-right corner of the bubble to copy that message’s text to clipboard.

---

### 3. Interaction Rules

| Action | Description |
|--------|--------------|
| Typing | User can type into the input box anytime |
| Send Button | Disabled **while** AI response is streaming |
| Streaming | Fetches from backend (`/ask`) and updates AI bubble progressively |
| Copy Button | Copies full text of message to clipboard |
| Storage | **No persistent storage** — no localStorage or session saving |
| Markdown | Supports bold, italics, inline code, code blocks, lists, etc. |

---

### 4. API Integration

The frontend communicates with the backend via:
```bash
POST http://localhost:8000/ask
Content-Type: application/json
Body: { "question": "user prompt here" }
````

The backend responds as a **streaming text response** (`text/plain`), which the frontend reads chunk-by-chunk using:

```js
const reader = response.body.getReader();
```

Each decoded chunk is appended to the AI’s active message in real time.

---

### 5. Component Layout Summary

#### 🧩 App Structure

```
src/
 ├── components/
 │    ├── Chat.tsx           # Main chat container logic
 │    ├── MessageBubble.tsx  # Message UI with markdown + copy button
 │    └── ChatInput.tsx      # Typing area + send button
 ├── App.tsx                 # Root layout (header + centered chat)
 ├── main.tsx                # React entrypoint
 └── index.css               # Tailwind base
```

#### 🧩 Layout Description

```text
 -----------------------------------------------------------
|                    AI Chat Interface                     |  <-- Header
 -----------------------------------------------------------
|                                                         |
|   [ AI Bubble ]                                         |
|                         [ User Bubble ]                 |
|   [ AI Bubble streaming... ]                            |  <-- Scrollable chat area (75% width)
|                                                         |
 -----------------------------------------------------------
|  [  typing input here  ][  Send ▶  ]                    |  <-- Fixed input area
 -----------------------------------------------------------
```

---

### 7. Streaming Logic (Frontend)

1. When the user clicks **Send**:

   * Disable the send button.
   * Immediately append the user message bubble.
   * Create a placeholder AI bubble with empty content.
2. Use `fetch()` to call `/ask`.
3. Read from the stream using:

   ```js
   const reader = res.body.getReader();
   while (true) {
     const { done, value } = await reader.read();
     if (done) break;
     const chunk = new TextDecoder().decode(value);
     update AI bubble content += chunk;
   }
   ```
4. Re-enable the send button once streaming is complete.

---

### 8. Markdown Rendering

Use:

```bash
npm install react-markdown remark-gfm
```

```tsx
<ReactMarkdown remarkPlugins={[remarkGfm]} className="prose prose-invert max-w-none">
  {message.content}
</ReactMarkdown>
```

---

### 9. Copy to Clipboard

Each bubble includes a small copy icon in its top-right corner:

```tsx
import { Clipboard } from "lucide-react";

<button
  onClick={() => navigator.clipboard.writeText(message.content)}
  className="absolute top-2 right-2 text-zinc-400 hover:text-white"
>
  <Clipboard size={14} />
</button>
```

---

## ✅ Expected Result

* Fully dark theme interface
* Centered chat interface occupying 75% of width
* No user login or storage (anonymous chat)
* Real-time streaming AI responses with inline Markdown rendering
* Send button disabled during streaming
* Copy-to-clipboard button on every chat bubble
* Smooth, minimal, professional UI using shadcn and Tailwind

---

## 🚀 Optional Enhancements

* Typing animation for streaming responses
* Scroll-to-bottom auto behavior
* Error handling for stream interruptions
* Loading indicator for AI typing

---

**End of Specification**
