#!/usr/bin/env python3
"""
AI Assistant - Main Launcher
Powered by Groq (Free API)

Usage:
  python main.py          → Choose mode interactively
  python main.py cli      → CLI mode directly
  python main.py web      → Web UI mode directly
  python main.py web 8080 → Web UI on custom port
"""

import sys
import os

CYAN  = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"

BANNER = f"""
{CYAN}{BOLD}
     █████╗    ██╗  ██╗   ██╗   ███████╗
    ██╔══██╗   ╚██╗██╔╝   ██║   ██╔════╝
    ███████║    ╚███╔╝    ██║   ███████╗
    ██╔══██║    ██╔██╗    ██║   ╚════██║
    ██║  ██║██╗██╔╝ ██╗██╗██║██╗███████║
    ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝╚═╝╚═╝╚══════╝
{RESET}
{DIM} Autonomus eXpert Intelligence System  {RESET}
{DIM}                          — Powered by Groq {RESET}
"""


def load_env():
    """Load .env file if present."""
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


def check_dependencies():
    """Check if required packages are installed."""
    missing = []
    try:
        import groq
    except ImportError:
        missing.append("groq")
    try:
        import flask
    except ImportError:
        missing.append("flask")

    if missing:
        print(f"\n{YELLOW}Missing packages: {', '.join(missing)}{RESET}")
        print(f"Run: {GREEN}pip install {' '.join(missing)}{RESET}\n")
        ans = input("Install now? (y/n): ").strip().lower()
        if ans == "y":
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing)
            print(f"{GREEN}✓ Installed!{RESET}\n")
        else:
            print("Please install manually and re-run.")
            sys.exit(1)


def get_api_key() -> str:
    """Get API key from env or prompt."""
    key = os.environ.get("GROQ_API_KEY", "")
    if key:
        masked = key[:6] + "..." + key[-4:]
        #print(f"{DIM}Using API key: {masked}{RESET}")
        return key

    print(f"\n{YELLOW}━━━ API Key Setup ━━━{RESET}")
    print(f"1. Go to {GREEN}https://console.groq.com{RESET}")
    print("2. Sign up (free, no credit card needed)")
    print("3. Click 'API Keys' → 'Create API Key'")
    print("4. Paste it below\n")

    key = input("Your Groq API Key: ").strip()
    if not key:
        print(f"\n{YELLOW}No key entered. Exiting.{RESET}")
        sys.exit(0)

    save = input("\nSave to .env for next time? (y/n): ").strip().lower()
    if save == "y":
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        with open(env_path, "a") as f:
            f.write(f"GROQ_API_KEY={key}\n")
        print(f"{GREEN}✓ Saved to .env{RESET}")

    os.environ["GROQ_API_KEY"] = key
    return key


def choose_mode() -> tuple:
    """Interactive mode selection."""
    print(f"\n{BOLD}Choose a mode:{RESET}\n")
    print(f"  {GREEN}1{RESET} → CLI  ")
    print(f"  {GREEN}2{RESET} → Web  ")
    print()

    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        return ("cli", 5000)
    elif choice == "2":
        port_str = input("Port? (default 5000): ").strip()
        port = int(port_str) if port_str.isdigit() else 5000
        return ("web", port)
    else:
        print(f"{YELLOW}Invalid choice. Defaulting to CLI.{RESET}")
        return ("cli", 5000)


def main():
    print(BANNER)
    load_env()
    check_dependencies()

    # Parse command-line args
    args = sys.argv[1:]
    if args:
        mode = args[0].lower()
        port = int(args[1]) if len(args) > 1 and args[1].isdigit() else 5000
    else:
        mode, port = choose_mode()

    api_key = get_api_key()

    print(f"\n{GREEN}Starting {mode.upper()} mode...{RESET}\n")

    if mode == "cli":
        # Add directory to path for imports
        sys.path.insert(0, os.path.dirname(__file__))
        os.environ["GROQ_API_KEY"] = api_key
        from cli import run_cli
        run_cli()

    elif mode == "web":
        sys.path.insert(0, os.path.dirname(__file__))
        from web import run_web
        run_web(api_key=api_key, port=port)

    else:
        print(f"Unknown mode: {mode}. Use 'cli' or 'web'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
