# 📐 AXIS: Autonomous eXpert Intelligence System
**Powered by Groq API — High Performance, No GPU Needed**

AXIS is a local developer tool providing a unified interface to interact with advanced cloud-hosted LLMs. It features a dual-mode system, letting you toggle between a terminal-native CLI and a browser-based Web UI without needing any local GPU compute resources.

---

## ⚡ Quick Start

### Step 1 — Get Your Free Groq API Key
1. Go to 👉 **https://console.groq.com**
2. Sign up and navigate to **"API Keys"** → **"Create API Key"**.
3. Copy the key for Step 3.

### Step 2 — Install Dependencies
Make sure you have Python 3.10+ installed, then run:
```bash
pip install groq flask
```
### Step 3 — Configure & Run AXIS
Create a .env file in the root directory of the project.

Add your API key exactly like this:

Code snippet
GROQ_API_KEY=your_actual_groq_api_key_here
Launch the application:

On Windows: Simply double-click axis.bat to boot the custom ASCII selection menu.

Via Terminal: Run the main routing launcher:

Bash
python main.py
🎮 Interface Modes
1. CLI Mode (Terminal-Native)
An interactive terminal workflow supporting local session management via text commands:

Command	Action
/help	Show all available internal commands
/clear	Wipe current conversation memory from the active list
/save	Export current chat history into a local JSON file
/load <file>	Restore a previous chat session from a saved JSON file
/summarize	Direct pipeline to process and condense pasted text blocks
/history	View the operational message count of the current session
/exit	Gracefully close the terminal interface

### 2. Web UI Mode (Browser-Based)
Spins up a local Flask web server. Open your preferred browser and navigate to:
👉 http://localhost:5000

📁 Repository Structure
AXIS-Autonomous-eXpert-Intelligence-System/
├── main.py       # Main router & launcher menu
├── core.py       # Core AI engine (Groq API wrapper & session arrays)
├── cli.py        # Terminal loop logic and slash commands
├── web.py        # Flask server backend & local UI routing
├── axis.bat      # Windows batch command shortcut menu
├── .gitignore    # Prevents private config files (.env) from leaking online
└── README.md     # This documentation

💡 Engine Tweaks & Configuration
The AI engine defaults to LLaMA 3.3 70B for premium output. If you want to alter the default models under the hood, open up core.py and modify the default string mapping:

Python
# Found inside core.py -> AIAssistant class constructor:
model: str = "llama-3.3-70b-versatile"   # Best quality reasoning (Default)
model: str = "llama-3.1-8b-instant"      # Ultra fast, lighter weights
model: str = "mixtral-8x7b-32768"        # Optimized for long context blocks

🗺️ Future Roadmap
- Persistent Database Integration: Moving from memory-based lists and JSON files to a structured local database tier.
- Dynamic Multi-LLM Orchestration: On-the-fly model toggling (Light, Balanced, Advanced) inside the UI/CLI.
- Workspace Context Reader: Feeding file path references directly into the LLM context.
- Multi-model Generation: Expanding workflows into text-to-image and image-to-video processing pipelines.
