import os
import time
from datetime import datetime

LOG_FILE = "file_changes.log"

def log_change(message):
    """Log changes with timestamp and print to console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)  # Show changes in console too
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

def monitor_folder(path):
    """Monitor specified folder for file changes"""
    if not os.path.exists(path):
        print(f" Error: Folder '{path}' does not exist!")
        print("Create the folder first or check the path.")
        return

    print(f" Monitoring folder: {path}")
    print(" Logging changes to:", os.path.abspath(LOG_FILE))
    print(" Press Ctrl+C to stop monitoring...\n")
    
    # Initialize with current state
    before = {
        f: os.path.getmtime(os.path.join(path, f)) 
        for f in os.listdir(path) 
        if os.path.isfile(os.path.join(path, f))
    }

    try:
        while True:
            time.sleep(3)  # Check interval (seconds)
            
            # Get current state
            after = {
                f: os.path.getmtime(os.path.join(path, f))
                for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))
            }

            # Detect changes
            added = set(after.keys()) - set(before.keys())
            removed = set(before.keys()) - set(after.keys())
            modified = {
                f for f in before.keys() & after.keys()
                if before[f] != after[f]
            }

            # Log changes
            if added: log_change(f" Added: {added}")
            if removed: log_change(f" Removed: {removed}")
            if modified: log_change(f" Modified: {modified}")

            before = after  # Update reference state

    except KeyboardInterrupt:
        print("\n Monitoring stopped by user.")
    except Exception as e:
        print(f"\n Error occurred: {str(e)}")

if __name__ == "__main__":
    target_folder = (r"C:\Users\asus\Desktop\Watcher\WatcherTest")
    monitor_folder(target_folder)