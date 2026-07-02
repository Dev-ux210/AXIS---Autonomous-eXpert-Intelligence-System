# 🤖 AI Assistant
**Powered by Groq (Free & Fast) — No GPU needed**

A Python AI chat app with CLI and Web UI modes, using the free Groq API running LLaMA 3.3 70B.

---

## ⚡ Quick Start (3 Steps)

### Step 1 — Get your FREE API key
1. Go to 👉 **https://console.groq.com**
2. Sign up (free, no credit card needed)
3. Click **"API Keys"** → **"Create API Key"**
4. Copy the key — you'll need it in Step 3

### Step 2 — Install Python dependencies
Open your terminal / command prompt and run:
```bash
pip install groq flask
```

### Step 3 — Run the app
```bash
python main.py
```
It will ask for your API key the first time, then let you pick CLI or Web mode.

---

## 🎮 Modes

### CLI Mode (Terminal)
```bash
python main.py cli
```
Chat directly in your terminal. Supports commands:

| Command | What it does |
|---------|-------------|
| `/help` | Show all commands |
| `/clear` | Wipe conversation memory |
| `/save` | Save chat to JSON file |
| `/load <file>` | Load a saved chat |
| `/summarize` | Paste text to summarize |
| `/history` | Show message count |
| `/exit` | Quit |

### Web UI Mode (Browser)
```bash
python main.py web
# or on a custom port:
python main.py web 8080
```
Opens a sleek dark chat interface at **http://localhost:5000**

---

## 📁 Project Structure
```
ai_assistant/
├── main.py      ← Start here (launcher)
├── core.py      ← AI engine (Groq API + memory)
├── cli.py       ← Terminal chat interface
├── web.py       ← Flask web server + HTML UI
├── .env         ← Your API key (auto-created)
└── README.md    ← This file
```

---

## 💡 Tips

**Save your API key permanently** — create a `.env` file:
```
GROQ_API_KEY=your_key_here
```

**Or set it as an environment variable:**
```bash
# Windows
set GROQ_API_KEY=your_key_here

# Mac/Linux
export GROQ_API_KEY=your_key_here
```

**Change the AI model** — edit `core.py`:
```python
model: str = "llama-3.3-70b-versatile"   # Best quality (default)
model: str = "llama-3.1-8b-instant"      # Faster, smaller
model: str = "mixtral-8x7b-32768"        # Great for long context
```

---

## 🆓 Free Groq Limits
- **1,000+ requests/day** on free tier
- No credit card required
- Extremely fast (200+ tokens/sec)
- Models: LLaMA 3.3 70B, Mixtral, Gemma

---

## 🔧 Requirements
- Python 3.10+
- `groq` package
- `flask` package (for web mode only)
- Internet connection (API calls)
- NO GPU needed!
