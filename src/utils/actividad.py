# utils/user_activity.py
import subprocess

def procssact():
    try:
        result = subprocess.run(["query", "user"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return result.stdout.strip().count('\n') + 1 if result.stdout.strip() else 1
    except Exception:
        pass
    return 0
