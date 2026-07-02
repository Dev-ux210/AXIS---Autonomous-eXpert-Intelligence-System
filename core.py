"""
Core AI engine - handles Groq API calls and conversation memory.
"""

import os
import json
from datetime import datetime

try:
    from groq import Groq
except ImportError:
    Groq = None

SYSTEM_PROMPT = """You are a helpful, smart, and concise AI assistant. 
You can help with coding, answering questions, summarizing text/PDFs, and general tasks.
Be direct and useful. If you don't know something, say so."""


class AIAssistant:
    def __init__(self, api_key: str = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY", "")
        self.model = model
        self.history = []
        self.client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            raise ValueError("No API key provided. Set GROQ_API_KEY env var or pass it directly.")
        if Groq is None:
            raise ImportError("groq package not installed. Run: pip install groq")
        self.client = Groq(api_key=self.api_key)

    def chat(self, user_message: str) -> str:
        """Send a message and get a response. Maintains conversation history."""
        self.history.append({"role": "user", "content": user_message})

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.history

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=2048,
                temperature=0.7,
            )
            reply = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.history.append({"role": "assistant", "content": error_msg})
            return error_msg

    def summarize(self, text: str) -> str:
        """Summarize a block of text."""
        prompt = f"Please summarize the following text concisely:\n\n{text}"
        return self.chat(prompt)

    def clear_history(self):
        """Reset conversation memory."""
        self.history = []

    def save_chat(self, filepath: str = None):
        """Save chat history to a JSON file."""
        if not filepath:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"chat_{ts}.json"
        with open(filepath, "w") as f:
            json.dump(self.history, f, indent=2)
        return filepath

    def load_chat(self, filepath: str):
        """Load a previous chat history."""
        with open(filepath, "r") as f:
            self.history = json.load(f)

    @property
    def message_count(self):
        return len(self.history)
