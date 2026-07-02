"""
Web UI mode - Flask server with a sleek dark chat interface.
"""

import os
import sys
import json

try:
    from flask import Flask, request, jsonify, render_template_string
except ImportError:
    print("Flask not installed. Run: pip install flask")
    sys.exit(1)

try:
    from core import AIAssistant
except ImportError:
    from ai_assistant.core import AIAssistant

app = Flask(__name__)
ai_instance = None

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>AXIS</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&family=Syne:wght@400;700;800&display=swap" rel="stylesheet"/>
<!-- Highlight.js for syntax highlighting -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<!-- marked.js for markdown parsing -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/9.1.6/marked.min.js"></script>
<style>
  :root {
    --bg: #0a0a0f;
    --surface: #111118;
    --surface2: #1a1a24;
    --border: #2a2a3a;
    --accent: #00d4aa;
    --accent2: #7c3aed;
    --text: #e2e8f0;
    --muted: #64748b;
    --user-bg: #1e1b4b;
    --ai-bg: #0f2027;
    --danger: #ef4444;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'JetBrains Mono', monospace;
    background: var(--bg);
    color: var(--text);
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
  }
  header {
    padding: 16px 24px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--surface);
    z-index: 10;
    flex-shrink: 0;
  }
  .logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .logo-dot {
    width: 10px; height: 10px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
  }
  .model-badge {
    font-size: 0.65rem;
    color: var(--muted);
    background: var(--surface2);
    border: 1px solid var(--border);
    padding: 4px 10px;
    border-radius: 20px;
    letter-spacing: 0.05em;
  }
  .header-actions { display: flex; gap: 8px; align-items: center; }
  .msg-count { font-size: 0.7rem; color: var(--muted); }
  .btn-clear {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    background: transparent;
    border: 1px solid var(--border);
    color: var(--muted);
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
  }
  .btn-clear:hover { border-color: var(--danger); color: var(--danger); }

  #chat-window {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    z-index: 1;
  }
  #chat-window::-webkit-scrollbar { width: 4px; }
  #chat-window::-webkit-scrollbar-track { background: transparent; }
  #chat-window::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

  .message {
    display: flex;
    flex-direction: column;
    max-width: 82%;
    animation: fadeUp 0.3s ease;
  }
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .message.user { align-self: flex-end; align-items: flex-end; }
  .message.ai   { align-self: flex-start; align-items: flex-start; }

  .msg-label {
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
    padding: 0 4px;
  }
  .message.user .msg-label { color: var(--accent2); }
  .message.ai   .msg-label { color: var(--accent); }

  .bubble {
    padding: 14px 18px;
    border-radius: 12px;
    font-size: 0.88rem;
    line-height: 1.7;
    word-break: break-word;
  }
  .message.user .bubble {
    background: var(--user-bg);
    border: 1px solid #312e81;
    border-bottom-right-radius: 3px;
    white-space: pre-wrap;
  }
  .message.ai .bubble {
    background: var(--ai-bg);
    border: 1px solid #164e63;
    border-bottom-left-radius: 3px;
  }

  /* ── Markdown rendered styles inside AI bubble ── */
  .bubble h1, .bubble h2, .bubble h3 {
    font-family: 'Syne', sans-serif;
    color: var(--accent);
    margin: 14px 0 6px;
    line-height: 1.3;
  }
  .bubble h1 { font-size: 1.1rem; border-bottom: 1px solid var(--border); padding-bottom: 6px; }
  .bubble h2 { font-size: 1rem; }
  .bubble h3 { font-size: 0.95rem; color: #a78bfa; }

  .bubble p { margin: 8px 0; }
  .bubble p:first-child { margin-top: 0; }
  .bubble p:last-child  { margin-bottom: 0; }

  .bubble strong { color: #f0f9ff; font-weight: 600; }
  .bubble em     { color: #a5f3fc; font-style: italic; }

  .bubble ul, .bubble ol {
    padding-left: 20px;
    margin: 8px 0;
  }
  .bubble li { margin: 4px 0; }
  .bubble li::marker { color: var(--accent); }

  /* Inline code */
  .bubble code {
    background: rgba(0, 212, 170, 0.1);
    color: var(--accent);
    padding: 2px 7px;
    border-radius: 5px;
    font-size: 0.85em;
    font-family: 'JetBrains Mono', monospace;
    border: 1px solid rgba(0, 212, 170, 0.2);
  }

  /* Code blocks */
  .bubble pre {
    margin: 12px 0;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border);
    position: relative;
  }
  .bubble pre code {
    background: transparent;
    color: inherit;
    padding: 0;
    border: none;
    font-size: 0.83rem;
    border-radius: 0;
    display: block;
  }
  /* Language label + copy button bar */
  .code-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #1e2030;
    padding: 6px 14px;
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
  }
  .code-lang { color: var(--accent); text-transform: uppercase; font-weight: 600; }
  .copy-btn {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    padding: 2px 8px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
  }
  .copy-btn:hover { border-color: var(--accent); color: var(--accent); }
  .copy-btn.copied { color: #4ade80; border-color: #4ade80; }

  /* hljs overrides to match theme */
  .hljs { background: #0d1117 !important; padding: 16px !important; }

  .bubble blockquote {
    border-left: 3px solid var(--accent2);
    padding-left: 12px;
    margin: 8px 0;
    color: var(--muted);
    font-style: italic;
  }
  .bubble hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 12px 0;
  }
  .bubble table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 0.83rem;
  }
  .bubble th {
    background: var(--surface2);
    color: var(--accent);
    padding: 8px 12px;
    text-align: left;
    border: 1px solid var(--border);
  }
  .bubble td {
    padding: 7px 12px;
    border: 1px solid var(--border);
  }
  .bubble tr:nth-child(even) td { background: rgba(255,255,255,0.02); }

  /* Typing indicator */
  .typing-indicator {
    display: flex;
    gap: 5px;
    padding: 14px 18px;
    background: var(--ai-bg);
    border: 1px solid #164e63;
    border-radius: 12px;
    border-bottom-left-radius: 3px;
    width: fit-content;
  }
  .typing-dot {
    width: 6px; height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: typingBounce 1.2s infinite;
  }
  .typing-dot:nth-child(2) { animation-delay: 0.2s; }
  .typing-dot:nth-child(3) { animation-delay: 0.4s; }
  @keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30%            { transform: translateY(-6px); opacity: 1; }
  }

  .input-area {
    padding: 16px 24px 20px;
    border-top: 1px solid var(--border);
    background: var(--surface);
    z-index: 10;
    flex-shrink: 0;
  }
  .input-row { display: flex; gap: 10px; align-items: flex-end; }
  #user-input {
    flex: 1;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    padding: 14px 16px;
    border-radius: 10px;
    resize: none;
    min-height: 50px;
    max-height: 150px;
    transition: border-color 0.2s;
    outline: none;
    line-height: 1.5;
  }
  #user-input:focus     { border-color: var(--accent); }
  #user-input::placeholder { color: var(--muted); }

  #send-btn {
    background: var(--accent);
    color: #000;
    border: none;
    padding: 14px 20px;
    border-radius: 10px;
    cursor: pointer;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    transition: all 0.2s;
    flex-shrink: 0;
  }
  #send-btn:hover    { background: #00f0c0; transform: translateY(-1px); }
  #send-btn:active   { transform: translateY(0); }
  #send-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

  .hint { font-size: 0.62rem; color: var(--muted); margin-top: 8px; text-align: center; }

  .empty-state {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    opacity: 0.4;
  }
  .empty-icon { font-size: 3rem; }
  .empty-text { font-family: 'Syne', sans-serif; font-size: 1rem; }
  .empty-sub  { font-size: 0.75rem; color: var(--muted); }
</style>
</head>
<body>

<header>
  <div class="logo">
    <div class="logo-dot"></div>
    AXIS
    <span class="model-badge" id="model-name">llama-3.3-70b</span>
  </div>
  <div class="header-actions">
    <span class="msg-count" id="msg-count">0 messages</span>
    <button class="btn-clear" onclick="clearChat()">/ clear</button>
  </div>
</header>

<div id="chat-window">
  <div class="empty-state" id="empty-state">
    <div class="empty-icon">⬡</div>
    <div class="empty-text">Assistant Ready</div>
    <div class="empty-sub">Ask anything — code, summaries, questions</div>
  </div>
</div>

<div class="input-area">
  <div class="input-row">
    <textarea id="user-input" placeholder="Type a message... (Shift+Enter for newline)" rows="1"></textarea>
    <button id="send-btn" onclick="sendMessage()">Send ↵</button>
  </div>
  <div class="hint">Enter to send &nbsp;·&nbsp; Shift+Enter for new line &nbsp;·&nbsp; /clear to reset memory</div>
</div>

<script>
  // ── Configure marked.js ──────────────────────────────────────
  marked.setOptions({
    breaks: true,       // newlines become <br>
    gfm: true,          // GitHub flavoured markdown
    highlight: null,    // we handle highlighting manually below
  });

  // Custom renderer to inject code-header bar above every code block
  const renderer = new marked.Renderer();
  renderer.code = function(code, language) {
    const lang = (language || 'text').toLowerCase();
    const validLang = hljs.getLanguage(lang) ? lang : 'plaintext';
    const highlighted = hljs.highlight(code, { language: validLang }).value;
    return `
      <pre>
        <div class="code-header">
          <span class="code-lang">${lang}</span>
          <button class="copy-btn" onclick="copyCode(this)">copy</button>
        </div>
        <code class="hljs language-${validLang}">${highlighted}</code>
      </pre>`;
  };
  marked.use({ renderer });

  // ── Copy button handler ──────────────────────────────────────
  function copyCode(btn) {
    const code = btn.closest('pre').querySelector('code').innerText;
    navigator.clipboard.writeText(code).then(() => {
      btn.textContent = 'copied ✓';
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = 'copy'; btn.classList.remove('copied'); }, 2000);
    });
  }

  // ── Chat state ───────────────────────────────────────────────
  let msgCount = 0;
  const chatWindow = document.getElementById('chat-window');
  const input      = document.getElementById('user-input');
  const sendBtn    = document.getElementById('send-btn');

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  });
  input.addEventListener('input', () => {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 150) + 'px';
  });

  // ── Add a message bubble ─────────────────────────────────────
  function addMessage(role, text) {
    const emptyState = document.getElementById('empty-state');
    if (emptyState) emptyState.remove();

    const wrap = document.createElement('div');
    wrap.className = `message ${role}`;

    const label = document.createElement('div');
    label.className = 'msg-label';
    label.textContent = role === 'user' ? '▶ you' : '⬡ ai';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    if (role === 'ai') {
      // Parse markdown for AI responses
      bubble.innerHTML = marked.parse(text);
    } else {
      // Plain text for user messages
      bubble.textContent = text;
    }

    wrap.appendChild(label);
    wrap.appendChild(bubble);
    chatWindow.appendChild(wrap);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    msgCount++;
    document.getElementById('msg-count').textContent = `${msgCount} messages`;
  }

  // ── Typing indicator ─────────────────────────────────────────
  function showTyping() {
    const wrap = document.createElement('div');
    wrap.className = 'message ai';
    wrap.id = 'typing';

    const label = document.createElement('div');
    label.className = 'msg-label';
    label.textContent = '⬡ ai';

    const ind = document.createElement('div');
    ind.className = 'typing-indicator';
    ind.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

    wrap.appendChild(label);
    wrap.appendChild(ind);
    chatWindow.appendChild(wrap);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }
  function removeTyping() {
    const el = document.getElementById('typing');
    if (el) el.remove();
  }

  // ── Send message ─────────────────────────────────────────────
  async function sendMessage() {
    const text = input.value.trim();
    if (!text || sendBtn.disabled) return;

    addMessage('user', text);
    input.value = '';
    input.style.height = 'auto';
    sendBtn.disabled = true;
    showTyping();

    try {
      const res  = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      removeTyping();
      addMessage('ai', data.response || data.error || 'No response');
    } catch (err) {
      removeTyping();
      addMessage('ai', 'Error: Could not reach the server.');
    }

    sendBtn.disabled = false;
    input.focus();
  }

  // ── Clear chat ───────────────────────────────────────────────
  async function clearChat() {
    await fetch('/clear', { method: 'POST' });
    chatWindow.innerHTML = '';
    msgCount = 0;
    document.getElementById('msg-count').textContent = '0 messages';
    const es = document.createElement('div');
    es.className = 'empty-state';
    es.id = 'empty-state';
    es.innerHTML = '<div class="empty-icon">⬡</div><div class="empty-text">Memory cleared</div><div class="empty-sub">Start a new conversation</div>';
    chatWindow.appendChild(es);
  }
</script>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():
    global ai_instance
    data = request.get_json()
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400
    response = ai_instance.chat(message)
    return jsonify({"response": response, "msg_count": ai_instance.message_count})


@app.route("/clear", methods=["POST"])
def clear():
    global ai_instance
    ai_instance.clear_history()
    return jsonify({"status": "cleared"})


@app.route("/status")
def status():
    global ai_instance
    return jsonify({
        "model": ai_instance.model if ai_instance else None,
        "msg_count": ai_instance.message_count if ai_instance else 0
    })


def run_web(api_key: str, port: int = 5000):
    global ai_instance
    ai_instance = AIAssistant(api_key=api_key)
    print(f"\n✓ AXIS Web UI running at: http://localhost:{port}")
    print(f"✓ Model: {ai_instance.model}")
    print(f"  Press Ctrl+C to stop\n")
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        key = input("Paste your Groq API key: ").strip()
    run_web(api_key=key)