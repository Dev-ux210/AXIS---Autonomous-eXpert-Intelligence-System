"""
CLI mode - Terminal-based chat interface with colors and commands.
"""

import os
import sys

# ANSI colors
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
RESET   = "\033[0m"

BANNER = f"""
{CYAN}{BOLD}
╔═══════════════════════════════════════════╗
║      🤖  AXiS AT YOUR SERVICE IN CLI      ║
╚═══════════════════════════════════════════╝
{RESET}"""

HELP_TEXT = f"""
{YELLOW}Available Commands:{RESET}
  {GREEN}/help{RESET}          - Show this help
  {GREEN}/clear{RESET}         - Clear conversation memory
  {GREEN}/save{RESET}          - Save chat history to file
  {GREEN}/load <file>{RESET}   - Load a previous chat
  {GREEN}/summarize{RESET}     - Paste text to summarize (end with /done)
  {GREEN}/history{RESET}       - Show message count
  {GREEN}/model{RESET}         - Show current model
  {GREEN}/exit{RESET}          - Quit

  {DIM}Just type normally to chat!{RESET}
"""


def render_markdown(text: str) -> str:
    """
    Convert basic Markdown to ANSI terminal formatting.
    Handles: code blocks, inline code, bold, headers, bullet points.
    """
    import re
    lines = text.split("\n")
    output = []
    in_code_block = False
    code_lang = ""

    for line in lines:
        # ── Code block fence ────────────────────────────────
        if line.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lang = line[3:].strip().upper()
                label = f" {code_lang} " if code_lang else " CODE "
                output.append(f"\n{BOLD}\033[48;5;235m\033[93m{label}{RESET}\033[48;5;235m")
            else:
                in_code_block = False
                output.append(f"{RESET}")
            continue

        if in_code_block:
            # Inside code block — green text on dark bg
            output.append(f"\033[48;5;235m{GREEN}{line}{RESET}")
            continue

        # ── Headers ─────────────────────────────────────────
        if line.startswith("### "):
            output.append(f"\n{YELLOW}{BOLD}{line[4:]}{RESET}")
            continue
        if line.startswith("## "):
            output.append(f"\n{CYAN}{BOLD}{line[3:]}{RESET}")
            continue
        if line.startswith("# "):
            output.append(f"\n{CYAN}{BOLD}{'━' * 40}{RESET}")
            output.append(f"{CYAN}{BOLD}  {line[2:]}{RESET}")
            output.append(f"{CYAN}{BOLD}{'━' * 40}{RESET}")
            continue

        # ── Bullet points ────────────────────────────────────
        if re.match(r"^[\*\-] ", line):
            content = line[2:]
            # Apply inline formatting to bullet content too
            content = _inline_format(content)
            output.append(f"  {CYAN}●{RESET} {content}")
            continue

        if re.match(r"^\d+\. ", line):
            m = re.match(r"^(\d+)\. (.*)", line)
            if m:
                content = _inline_format(m.group(2))
                output.append(f"  {CYAN}{m.group(1)}.{RESET} {content}")
            continue

        # ── Regular line with inline formatting ─────────────
        output.append(_inline_format(line))

    return "\n".join(output)


def _inline_format(text: str) -> str:
    """Apply inline markdown: **bold**, `code`, *italic*."""
    import re
    # Bold: **text**
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: f"{BOLD}{m.group(1)}{RESET}", text)
    # Inline code: `code`
    text = re.sub(r"`([^`]+)`", lambda m: f"\033[48;5;235m{GREEN} {m.group(1)} {RESET}", text)
    # Italic: *text*
    text = re.sub(r"\*(.+?)\*", lambda m: f"\033[3m{m.group(1)}{RESET}", text)
    return text


def print_response(text: str):
    """Print AI response with markdown rendering."""
    print(f"\n{CYAN}{BOLD}AI:{RESET}")
    rendered = render_markdown(text)
    print(rendered)
    print()


def get_api_key() -> str:
    """Get API key from env or prompt user."""
    key = os.environ.get("GROQ_API_KEY", "")
    if key:
        return key
    print(f"\n{YELLOW}No GROQ_API_KEY found in environment.{RESET}")
    print(f"{DIM}Get a free key at: https://console.groq.com{RESET}\n")
    key = input("Paste your Groq API key: ").strip()
    if not key:
        print(f"{RED}No API key provided. Exiting.{RESET}")
        sys.exit(1)
    # Offer to save it
    save = input("Save key to .env file for next time? (y/n): ").strip().lower()
    if save == "y":
        with open(".env", "a") as f:
            f.write(f"\nGROQ_API_KEY={key}\n")
        print(f"{GREEN}Saved to .env ✓{RESET}")
    return key


def handle_summarize(ai) -> None:
    """Multi-line text input for summarization."""
    print(f"\n{YELLOW}Paste the text you want summarized.")
    print(f"Type /done on a new line when finished:{RESET}\n")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "/done":
                break
            lines.append(line)
        except EOFError:
            break
    if not lines:
        print(f"{RED}No text provided.{RESET}")
        return
    text = "\n".join(lines)
    print(f"\n{DIM}Summarizing...{RESET}")
    result = ai.summarize(text)
    print_response(result)


def run_cli():
    """Main CLI loop."""
    print(BANNER)

    # Load .env if present
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

    api_key = get_api_key()

    try:
        from core import AIAssistant
    except ImportError:
        from ai_assistant.core import AIAssistant

    try:
        ai = AIAssistant(api_key=api_key)
        print(f"\n{GREEN}✓ Connected to AXIS | Model: {ai.model}{RESET}")
        print(f"{DIM}Type /help for commands or just start chatting!{RESET}\n")
    except Exception as e:
        print(f"{RED}Failed to connect: {e}{RESET}")
        sys.exit(1)

    while True:
        try:
            user_input = input(f"{BOLD}>> {RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{DIM}Goodbye!{RESET}\n")
            break

        if not user_input:
            continue

        # Commands
        if user_input.startswith("/"):
            cmd = user_input.split()[0].lower()

            if cmd == "/exit":
                print(f"\n{DIM}Goodbye!{RESET}\n")
                break

            elif cmd == "/help":
                print(HELP_TEXT)

            elif cmd == "/clear":
                ai.clear_history()
                print(f"{GREEN}✓ Conversation memory cleared.{RESET}\n")

            elif cmd == "/save":
                path = ai.save_chat()
                print(f"{GREEN}✓ Chat saved to: {path}{RESET}\n")

            elif cmd == "/load":
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    print(f"{RED}Usage: /load <filename>{RESET}\n")
                else:
                    try:
                        ai.load_chat(parts[1])
                        print(f"{GREEN}✓ Loaded chat from: {parts[1]}{RESET}\n")
                    except FileNotFoundError:
                        print(f"{RED}File not found: {parts[1]}{RESET}\n")

            elif cmd == "/summarize":
                handle_summarize(ai)

            elif cmd == "/history":
                print(f"{YELLOW}Messages in memory: {ai.message_count}{RESET}\n")

            elif cmd == "/model":
                print(f"{YELLOW}Current model: {ai.model}{RESET}\n")

            else:
                print(f"{RED}Unknown command. Type /help for a list.{RESET}\n")

        else:
            # Regular chat
            print(f"\n{DIM}Thinking...{RESET}", end="\r")
            response = ai.chat(user_input)
            print_response(response)


if __name__ == "__main__":
    run_cli()