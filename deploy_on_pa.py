import requests
import time
import sys
import json

USERNAME = "kaushalahirwar714"
TOKEN = "e6349077c1af3ee730e05a036b2ef0afbb69dd53"
GITHUB_URL = "https://github.com/kaushalahirwar21/choudhary-travels.git"
API_BASE = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}"

HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

def create_console():
    res = requests.post(
        f"{API_BASE}/consoles/",
        headers=HEADERS,
        json={"executable": "bash"}
    )
    if res.status_code == 201:
        return res.json()["id"]
    print("Failed to create console:", res.text)
    sys.exit(1)

def send_input(console_id, command):
    # send input
    res = requests.post(
        f"{API_BASE}/consoles/{console_id}/send_input/",
        headers=HEADERS,
        json={"input": command + "\n"}
    )
    return res.status_code == 200

def get_output(console_id):
    res = requests.get(
        f"{API_BASE}/consoles/{console_id}/get_latest_output/",
        headers=HEADERS
    )
    if res.status_code == 200:
        return res.json()["output"]
    return ""

def main():
    print("🚀 Starting deployment to PythonAnywhere...")
    print("Creating bash console...")
    c_id = create_console()
    print(f"Console ID: {c_id}")
    time.sleep(2)
    
    print("Sending installation command (this takes several minutes, please be patient)...")
    
    # Run pip install, wait for success, then configure django
    deploy_cmd = f"pip3.10 install --user pythonanywhere && pa_autoconfigure_django.py --python=3.10 {GITHUB_URL}"
    send_input(c_id, deploy_cmd)
    
    print("Waiting for deployment script to finish. Continuously streaming output:")
    last_output = ""
    while True:
        try:
            out = get_output(c_id)
            if out is not None and len(out) > len(last_output):
                new_chunk = out[len(last_output):]
                print(new_chunk, end="", flush=True)
                last_output = out
            if "All done!" in out or "Error:" in out or "Traceback" in out:
                break
            time.sleep(5)
        except KeyboardInterrupt:
            break
            
    print("\n✅ Deployment finished! Check https://kaushalahirwar714.pythonanywhere.com")

if __name__ == "__main__":
    main()
