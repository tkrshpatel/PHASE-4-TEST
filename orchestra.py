# orchestrator.py
import os, csv, json, time, threading, requests, webbrowser, pyautogui, pygetwindow as gw, pyperclip
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import load_dotenv
from channels_list import get_joined_channel_ids

# -------------------------
# Setup
# -------------------------
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
API_KEY = os.getenv("API_KEY_EARNKARO")
API_URL = "https://ekaro-api.affiliaters.in/api/converter/public"
CSV_FILE = "telegram_messages.csv"

# Ensure CSV exists
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["DateTime", "ChannelLink", "OriginalMessage", "DirectMessage", "UpdatedMessage", "Status"])

csv_lock = threading.Lock()

# -------------------------
# CSV Utilities
# -------------------------
def read_csv():
    with csv_lock:
        with open(CSV_FILE, "r", newline='', encoding="utf-8") as f:
            return list(csv.reader(f))

def write_csv(header, rows):
    with csv_lock:
        with open(CSV_FILE, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)

def append_csv(row):
    with csv_lock:
        with open(CSV_FILE, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

# -------------------------
# Telegram Worker
# -------------------------
client = TelegramClient('session_name', api_id, api_hash)
channels_to_monitor = get_joined_channel_ids()

@client.on(events.NewMessage(chats=channels_to_monitor))
async def handler(event):
    msg_text = event.message.message.strip()
    if not msg_text:
        return
    msg_datetime = event.message.date.strftime("%Y-%m-%d %H:%M:%S")
    sender = await event.get_chat()
    username = getattr(sender, "username", None)
    message_id = event.message.id
    channel_link = f"https://t.me/{username}/{message_id}" if username else "N/A"
    append_csv([msg_datetime, channel_link, msg_text, "", "", "TBS"])
    print(f"📝 New Telegram message queued: {msg_text[:60]}...")

# -------------------------
# API Worker
# -------------------------
def convert_message_via_api(message):
    payload = json.dumps({"deal": message, "convert_option": "convert_only"})
    headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
    try:
        response = requests.post(API_URL, headers=headers, data=payload, timeout=15)
        if response.status_code == 200:
            return response.json().get("data", "").strip()
        return f"API_ERROR: {response.text}"
    except Exception as e:
        return f"API_EXCEPTION: {e}"

def api_worker():
    while True:
        data = read_csv()
        header, rows = data[0], data[1:]
        changed = False
        updated_rows = []
        for row in rows:
            if row[5] == "TBS":
                print(f"🔄 API processing: {row[2][:60]}...")
                updated_msg = convert_message_via_api(row[2])
                if not updated_msg or "We could not find" in updated_msg.lower() or updated_msg.startswith("API_"):
                    row[4] = updated_msg
                    row[5] = "ERROR"
                else:
                    row[4] = updated_msg
                    row[5] = "LU"
                changed = True
            updated_rows.append(row)
        if changed:
            write_csv(header, updated_rows)
            print("✅ API updates saved to CSV")
        time.sleep(5)

# -------------------------
# WhatsApp Worker
# -------------------------
def restore_whatsapp_window():
    for window in gw.getWindowsWithTitle("WhatsApp"):
        if window.isMinimized:
            window.restore(); window.maximize(); return True
        elif not window.isActive:
            window.activate(); window.maximize(); return True
    return False

def is_whatsapp_web_open():
    return any("WhatsApp" in title or "web.whatsapp.com" in title for title in gw.getAllTitles())

def WA_setup():
    if not is_whatsapp_web_open():
        webbrowser.open("https://web.whatsapp.com")
        print("⏳ Waiting for WhatsApp Web...")
        time.sleep(15)
    pyautogui.FAILSAFE = True
    pyautogui.click(49, 244)   # adjust manually
    time.sleep(0.5)
    pyautogui.click(283, 284)  # adjust manually
    time.sleep(1)

def send_message(msg):
    WA_setup()
    restore_whatsapp_window()
    print(f"📤 Sending WhatsApp message:\n{msg[:60]}...")
    pyautogui.click(852, 1089)  # adjust manually
    time.sleep(0.5)
    pyperclip.copy(msg)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(1)
    print("✅ WhatsApp sent!")

def whatsapp_worker():
    while True:
        data = read_csv()
        header, rows = data[0], data[1:]
        recent_msgs = [row[4].lower().strip() for row in rows if row[5] == "SENT"]
        changed = False
        updated_rows = []
        for row in rows:
            if row[5] == "LU":
                msg = row[4].strip()
                if not msg or "we could not find" in msg.lower() or "api_" in msg.lower():
                    row[5] = "ERROR"
                elif msg.lower() in recent_msgs[-5:]:
                    row[5] = "DUPLICATE"
                else:
                    send_message(msg)
                    row[5] = "SENT"
                    recent_msgs.append(msg.lower())
                changed = True
            updated_rows.append(row)
        if changed:
            write_csv(header, updated_rows)
        time.sleep(3)

# -------------------------
# Run all workers
# -------------------------
if __name__ == "__main__":
    threading.Thread(target=api_worker, daemon=True).start()
    threading.Thread(target=whatsapp_worker, daemon=True).start()

    # Proper way to run Telethon client
    with client:
        print("🚀 Orchestrator running (Telegram + API + WhatsApp)")
        client.run_until_disconnected()

