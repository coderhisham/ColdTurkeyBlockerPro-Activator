import json
import os
import platform
import sqlite3
import sys
import time
from datetime import datetime


def print_banner():
    banner = """
    🔓 Cold Turkey PRO for FREE 🔓
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    print(banner)


def get_db_path():
    system = platform.system()

    if system == "Windows":
        return r"C:/ProgramData/Cold Turkey/data-app.db"
    elif system == "Darwin":  # macOS
        return r"/Library/Application Support/Cold Turkey/data-app.db"
    else:
        print("❌ Unsupported operating system:", system)
        sys.exit(1)


def kill_cold_turkey():
    system = platform.system()
    
    if system == "Darwin":
        os.system("killall 'Cold Turkey Blocker'")  # macOS process name
    elif system == "Windows":
        os.system("taskkill /f /im 'Cold Turkey Blocker.exe' >nul 2>&1")  # Optional for Windows


def show_spinner(seconds, message="Processing"):
    """Display a spinning animation while processing"""
    if not sys.stdout.isatty():
        time.sleep(seconds)
        return
        
    spinner = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    start_time = time.time()
    i = 0
    
    try:
        while time.time() - start_time < seconds:
            sys.stdout.write(f"\r{spinner[i % len(spinner)]} {message}")
            sys.stdout.flush()
            i += 1
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r')
        sys.stdout.flush()
    except KeyboardInterrupt:
        sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r')
        sys.stdout.flush()
        raise


def activate(db_path):
    try:
        print("🔌 Connecting to database...")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        print("🔍 Reading current configuration...")
        show_spinner(0.8, "Reading settings")
        
        row = c.execute("SELECT value FROM settings WHERE key = 'settings'").fetchone()
        if not row or not row[0]:
            print("⚠️ No valid data found in settings.")
            return

        raw = row[0]
        
        try:
            print("🧩 Parsing configuration data...")
            show_spinner(0.7, "Analyzing settings")
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print("❌ Failed to decode JSON:", e)
            return

        current_status = data.get("additional", {}).get("proStatus", "unknown")

        if current_status != "pro":
            print("🔑 Modifying license status...")
            show_spinner(1, "Applying PRO license")
            data["additional"]["proStatus"] = "pro"
            print("✅ Cold Turkey PRO activated successfully! 🚀")
        else:
            data["additional"]["proStatus"] = "free"
            print("ℹ️ Cold Turkey was already activated. Now deactivated. ⏬")

        # Update DB
        print("💾 Saving changes to database...")
        show_spinner(0.8, "Committing changes")
        c.execute("UPDATE settings SET value = ? WHERE key = 'settings'", (json.dumps(data),))
        conn.commit()
        print("✨ Changes committed successfully!")

    except sqlite3.Error as e:
        print("❌ Database error:", e)

    finally:
        if conn:
            conn.close()
        print("🔄 Restarting Cold Turkey application...")
        kill_cold_turkey()


def main():
    print_banner()
    
    print(f"🖥️  System: {platform.system()} {platform.release()}")
    print("🔎 Locating Cold Turkey database...")
    show_spinner(0.7, "Searching for database")
    
    db_path = get_db_path()
    
    if os.path.exists(db_path):
        print(f"✅ Database found at {db_path}")
        
        activate(db_path)
        
        print("\n" + "─" * 50)
        print("⭐ If you found this helpful, please star the repo!")
        print("   https://github.com/coderhisham/ColdTurkeyBlockerPro-Activator-FREE")
        print("🐛 Found a bug? Open an issue on GitHub!")
        print("─" * 50 + "\n")
    else:
        print("❌ Database not found at", db_path)
        print("💡 Cold Turkey Blocker needs to be installed and run once.")
        print("🔄 Please install and run Cold Turkey Blocker first, then try again.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        sys.exit(0)