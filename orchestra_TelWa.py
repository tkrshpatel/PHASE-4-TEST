# # import os, csv, json, time, threading, requests, webbrowser, pyautogui, pygetwindow as gw, pyperclip, re
# # from datetime import datetime
# # from telethon import TelegramClient, events
# # from dotenv import load_dotenv
# # from channels_list import get_joined_channel_ids

# # # -------------------------
# # # Setup
# # # -------------------------
# # load_dotenv()
# # api_id = os.getenv("API_ID")
# # api_hash = os.getenv("API_HASH")
# # API_KEY = os.getenv("API_KEY_EARNKARO")
# # BOT_TOKEN = os.getenv("BOT_TOKEN")
# # CHANNEL_ID = os.getenv("CHANNEL_ID")  # e.g. "@mychannelusername"
# # API_URL = "https://ekaro-api.affiliaters.in/api/converter/public"
# # CSV_FILE = "telegram_messages.csv"

# # if not os.path.isfile(CSV_FILE):
# #     with open(CSV_FILE, "w", newline='', encoding="utf-8") as f:
# #         writer = csv.writer(f)
# #         writer.writerow(["DateTime", "ChannelLink", "OriginalMessage", "DirectMessage", "UpdatedMessage", "Status"])

# # csv_lock = threading.Lock()

# # # -------------------------
# # # CSV Utilities
# # # -------------------------
# # def read_csv():
# #     with csv_lock:
# #         with open(CSV_FILE, "r", newline='', encoding="utf-8") as f:
# #             return list(csv.reader(f))

# # def write_csv(header, rows):
# #     with csv_lock:
# #         with open(CSV_FILE, "w", newline='', encoding="utf-8") as f:
# #             writer = csv.writer(f)
# #             writer.writerow(header)
# #             writer.writerows(rows)

# # def append_csv(row):
# #     with csv_lock:
# #         with open(CSV_FILE, "a", newline='', encoding="utf-8") as f:
# #             writer = csv.writer(f)
# #             writer.writerow(row)

# # # -------------------------
# # # Telegram Worker (Monitor)
# # # -------------------------
# # client = TelegramClient('session_name', api_id, api_hash)
# # channels_to_monitor = get_joined_channel_ids()

# # @client.on(events.NewMessage(chats=channels_to_monitor))
# # async def handler(event):
# #     msg_text = event.message.message.strip()
# #     if not msg_text:
# #         return
# #     msg_datetime = event.message.date.strftime("%Y-%m-%d %H:%M:%S")
# #     sender = await event.get_chat()
# #     username = getattr(sender, "username", None)
# #     message_id = event.message.id
# #     channel_link = f"https://t.me/{username}/{message_id}" if username else "N/A"
# #     append_csv([msg_datetime, channel_link, msg_text, "", "", "TBS"])
# #     print(f"📝 New Telegram message queued: {msg_text[:60]}...")

# # # -------------------------
# # # API Worker
# # # -------------------------
# # def convert_message_via_api(message):
# #     payload = json.dumps({"deal": message, "convert_option": "convert_only"})
# #     headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
# #     try:
# #         response = requests.post(API_URL, headers=headers, data=payload, timeout=15)
# #         if response.status_code == 200:
# #             return response.json().get("data", "").strip()
# #         return f"API_ERROR: {response.text}"
# #     except Exception as e:
# #         return f"API_EXCEPTION: {e}"

# # def api_worker():
# #     while True:
# #         data = read_csv()
# #         header, rows = data[0], data[1:]
# #         changed = False
# #         updated_rows = []
# #         for row in rows:
# #             if row[5] == "TBS":
# #                 print(f"🔄 API processing: {row[2][:60]}...")
# #                 updated_msg = convert_message_via_api(row[2])
# #                 if not updated_msg or "We could not find" in updated_msg.lower() or updated_msg.startswith("API_"):
# #                     row[4] = updated_msg
# #                     row[5] = "ERROR"
# #                 else:
# #                     row[4] = updated_msg
# #                     row[5] = "LU"
# #                 changed = True
# #             updated_rows.append(row)
# #         if changed:
# #             write_csv(header, updated_rows)
# #             print("✅ API updates saved to CSV")
# #         time.sleep(5)

# # # -------------------------
# # # WhatsApp Worker
# # # -------------------------
# # def restore_whatsapp_window():
# #     for window in gw.getWindowsWithTitle("WhatsApp"):
# #         if window.isMinimized:
# #             window.restore(); window.maximize(); pyautogui.click(852, 1089); return True
# #         elif not window.isActive:
# #             window.activate(); window.maximize(); pyautogui.click(852, 1089); return True
# #     return False

# # def is_whatsapp_web_open():
# #     return any("WhatsApp" in title or "web.whatsapp.com" in title for title in gw.getAllTitles())

# # def WA_setup():
# #     if not is_whatsapp_web_open():
# #         webbrowser.open("https://web.whatsapp.com")
# #         print("⏳ Waiting for WhatsApp Web...")
# #         time.sleep(15)
# #     pyautogui.FAILSAFE = True
# #     pyautogui.click(49, 244)   # adjust manually
# #     time.sleep(0.5)
# #     pyautogui.click(283, 284)  # adjust manually
# #     time.sleep(1)


# # def send_to_whatsapp(msg):
# #     # -------------------
# #     # 1. Remove unwanted "Join us / Join our" lines
# #     # -------------------
# #     # cleaned_lines = []
# #     # for line in msg.splitlines():
# #     #     if re.search(r"(join\s+us|join\s+our|join\s+our\s+whatsapp)", line, re.IGNORECASE):
# #     #         continue  # skip this line entirely
# #     #     cleaned_lines.append(line.strip())
    
# #     # msg = "\n".join([l for l in cleaned_lines if l])  # remove blank lines

# #     # # -------------------
# #     # # 2. Append your signature block (with bold parts)
# #     # # -------------------
# #     # msg += (
# #     #     "\n\n-------------------------------------\n"
# #     #     "*Join us at:*\n"
# #     #     "WhatsApp: https://tinyurl.com/SuperDeals1dot0\n"
# #     #     "Telegram: https://t.me/superdeal1dot0"
# #     # )

# #     # -------------------
# #     # WhatsApp sending automation
# #     # -------------------
# #     WA_setup()
# #     restore_whatsapp_window()
# #     print(f"📤 Sending WhatsApp message:\n{msg[:60]}...")

# #     pyautogui.click(852, 1089)  # adjust manually
# #     pyperclip.copy(msg)
# #     pyautogui.hotkey("ctrl", "v")
# #     time.sleep(0.2)
# #     pyautogui.press("enter")
# #     time.sleep(1)
# #     print("✅ WhatsApp sent!")


# # # -------------------------
# # # Telegram Channel Poster
# # # -------------------------
# # def send_to_channel(message):
# #     url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
# #     payload = {
# #         "chat_id": CHANNEL_ID,
# #         "text": message,
# #         "parse_mode": "HTML"
# #     }
# #     response = requests.post(url, data=payload)
# #     if response.status_code == 200:
# #         print("✅ Message sent to Telegram channel")
# #     else:
# #         print(f"❌ Failed to send to channel: {response.status_code}, {response.text}")

# # # -------------------------
# # # Worker for sending LU messages
# # # -------------------------
# # def sending_worker():
# #     recent_msgs = []
# #     while True:
# #         data = read_csv()
# #         header, rows = data[0], data[1:]
# #         changed = False
# #         updated_rows = []
# #         for row in rows:
# #             if row[5] == "LU":
# #                 msg = row[4].strip()
# #                 if not msg or msg.lower().startswith("we could not locate") or msg.lower().startswith("api_"):
# #                     row[5] = "ERROR"
# #                 elif msg.lower() in recent_msgs[-5:]:
# #                     row[5] = "DUPLICATE"
                
# #                 else:
# #                     # Remove text
# #                     cleaned_lines = []
# #                     for line in msg.splitlines():
# #                         if re.search(r"(join\s+us|join\s+our|join\s+our\s+whatsapp)", line, re.IGNORECASE):
# #                             continue  # skip this line entirely
# #                         cleaned_lines.append(line.strip())
                    
# #                     msg = "\n".join([l for l in cleaned_lines if l])  # remove blank lines

# #                     # -------------------
# #                     # 2. Append your signature block (with bold parts)
# #                     # -------------------
# #                     msg += (
# #                         "\n\n-------------------------------------\n"
# #                         "*Join us at:*\n"
# #                         "WhatsApp: https://tinyurl.com/SuperDeals1dot0\n"
# #                         "Telegram: https://t.me/superdeal1dot0"
# #                     )
# #                     # Send 
# #                     send_to_channel(msg)
# #                     time.sleep(1)
                    
# #                     #send_to_whatsapp(msg)
                    
# #                     row[5] = "SENT"
# #                     recent_msgs.append(msg.lower())
# #                 changed = True
# #             updated_rows.append(row)
# #         if changed:
# #             write_csv(header, updated_rows)
# #         time.sleep(1)

# # # -------------------------
# # # Run all workers
# # # -------------------------
# # if __name__ == "__main__":
# #     threading.Thread(target=api_worker, daemon=True).start()
# #     threading.Thread(target=sending_worker, daemon=True).start()
# #     with client:
# #         print("🚀 Orchestrator running (Telegram + API + WhatsApp + Channel)")
# #         client.run_until_disconnected()



# import os, csv, json, time, threading, requests, webbrowser, pyautogui, pygetwindow as gw, pyperclip, re
# from datetime import datetime
# from telethon import TelegramClient, events
# from dotenv import load_dotenv
# from channels_list import get_joined_channel_ids

# # -------------------------
# # Setup
# # -------------------------
# load_dotenv()
# api_id = os.getenv("API_ID")
# api_hash = os.getenv("API_HASH")
# API_KEY = os.getenv("API_KEY_EARNKARO")
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# CHANNEL_ID = os.getenv("CHANNEL_ID")
# API_URL = "https://ekaro-api.affiliaters.in/api/converter/public"
# CSV_FILE = "telegram_messages.csv"

# # Validate critical configs
# for key, val in {
#     "API_ID": api_id, "API_HASH": api_hash, "API_KEY": API_KEY,
#     "BOT_TOKEN": BOT_TOKEN, "CHANNEL_ID": CHANNEL_ID
# }.items():
#     if not val:
#         raise EnvironmentError(f"❌ Missing required environment variable: {key}")

# # Create CSV if missing
# if not os.path.isfile(CSV_FILE):
#     with open(CSV_FILE, "w", newline='', encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow(["DateTime", "ChannelLink", "OriginalMessage", "DirectMessage", "UpdatedMessage", "Status"])

# csv_lock = threading.Lock()

# # -------------------------
# # CSV Utilities
# # -------------------------
# def read_csv():
#     with csv_lock:
#         try:
#             with open(CSV_FILE, "r", newline='', encoding="utf-8") as f:
#                 return list(csv.reader(f))
#         except Exception as e:
#             print(f"⚠️ Error reading CSV: {e}")
#             return [[]]

# def write_csv(header, rows):
#     with csv_lock:
#         try:
#             with open(CSV_FILE, "w", newline='', encoding="utf-8") as f:
#                 writer = csv.writer(f)
#                 writer.writerow(header)
#                 writer.writerows(rows)
#         except Exception as e:
#             print(f"⚠️ Error writing CSV: {e}")

# def append_csv(row):
#     with csv_lock:
#         with open(CSV_FILE, "a", newline='', encoding="utf-8") as f:
#             csv.writer(f).writerow(row)

# # -------------------------
# # Telegram Worker (Monitor)
# # -------------------------
# client = TelegramClient('session_name', api_id, api_hash)
# channels_to_monitor = get_joined_channel_ids()

# @client.on(events.NewMessage(chats=channels_to_monitor))
# async def handler(event):
#     msg_text = (event.message.message or "").strip()
#     if not msg_text:
#         return
#     msg_datetime = event.message.date.strftime("%Y-%m-%d %H:%M:%S")
#     sender = await event.get_chat()
#     username = getattr(sender, "username", None)
#     message_id = event.message.id
#     channel_link = f"https://t.me/{username}/{message_id}" if username else "N/A"
#     append_csv([msg_datetime, channel_link, msg_text, "", "", "TBS"])
#     print(f"📝 Queued message from Telegram: {msg_text[:60]}...")

# # -------------------------
# # API Worker
# # -------------------------
# def convert_message_via_api(message):
#     payload = json.dumps({"deal": message, "convert_option": "convert_only"})
#     headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
#     try:
#         response = requests.post(API_URL, headers=headers, data=payload, timeout=20)
#         if response.status_code == 200:
#             return response.json().get("data", "").strip()
#         else:
#             return f"API_ERROR: {response.text}"
#     except Exception as e:
#         return f"API_EXCEPTION: {e}"

# def api_worker():
#     while True:
#         try:
#             data = read_csv()
#             if not data or len(data) < 2:
#                 time.sleep(5)
#                 continue
#             header, rows = data[0], data[1:]
#             changed = False
#             updated_rows = []
#             for row in rows:
#                 if len(row) < 6:
#                     continue
#                 if row[5] == "TBS":
#                     print(f"🔄 Converting via API: {row[2][:60]}...")
#                     updated_msg = convert_message_via_api(row[2])
#                     if not updated_msg or "We could not find" in updated_msg.lower() or updated_msg.startswith("API_"):
#                         row[4], row[5] = updated_msg, "ERROR"
#                     else:
#                         row[4], row[5] = updated_msg, "LU"
#                     changed = True
#                 updated_rows.append(row)
#             if changed:
#                 write_csv(header, updated_rows)
#                 print("✅ API updates saved to CSV")
#             time.sleep(5)
#         except Exception as e:
#             print(f"⚠️ Error in API worker: {e}")
#             time.sleep(5)

# # -------------------------
# # WhatsApp Automation (optional)
# # -------------------------
# def restore_whatsapp_window():
#     for window in gw.getWindowsWithTitle("WhatsApp"):
#         if window.isMinimized:
#             window.restore()
#         window.activate()
#         window.maximize()
#         pyautogui.click(852, 1089)
#         return True
#     return False

# def is_whatsapp_web_open():
#     return any("WhatsApp" in t or "web.whatsapp.com" in t for t in gw.getAllTitles())

# def WA_setup():
#     if not is_whatsapp_web_open():
#         webbrowser.open("https://web.whatsapp.com")
#         print("⏳ Waiting for WhatsApp Web...")
#         time.sleep(15)
#     pyautogui.FAILSAFE = True
#     pyautogui.click(49, 244)
#     time.sleep(0.5)
#     pyautogui.click(283, 284)
#     time.sleep(1)

# def send_to_whatsapp(msg):
#     WA_setup()
#     #restore_whatsapp_window()
#     print(f"📤 Sending WhatsApp message:\n{msg[:60]}...")
#     pyautogui.click(852, 1089)
#     pyperclip.copy(msg)
#     pyautogui.hotkey("ctrl", "v")
#     time.sleep(0.3)
#     pyautogui.press("enter")
#     time.sleep(1)
#     print("✅ WhatsApp sent!")

# # -------------------------
# # Telegram Channel Poster
# # -------------------------
# def send_to_channel(message):
#     try:
#         url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
#         payload = {"chat_id": CHANNEL_ID, "text": message, "parse_mode": "Markdown"}
#         response = requests.post(url, data=payload)
#         if response.status_code == 200:
#             print("✅ Message sent to Telegram channel")
#         else:
#             print(f"❌ Failed to send: {response.status_code}, {response.text}")
#     except Exception as e:
#         print(f"⚠️ Telegram channel send error: {e}")

# # -------------------------
# # Sending Worker (LU messages)
# # -------------------------
# def sending_worker():
#     recent_msgs = []
#     while True:
#         try:
#             data = read_csv()
#             if not data or len(data) < 2:
#                 time.sleep(2)
#                 continue
#             header, rows = data[0], data[1:]
#             changed = False
#             updated_rows = []
#             for row in rows:
#                 if len(row) < 6:
#                     continue
#                 if row[5] == "LU":
#                     msg = row[4].strip()
#                     if not msg or msg.lower().startswith(("we could not locate", "api_")):
#                         row[5] = "ERROR"
#                     elif msg.lower() in recent_msgs[-5:]:
#                         row[5] = "DUPLICATE"
#                     else:
#                         # Clean + Append Signature
#                         cleaned_lines = [l.strip() for l in msg.splitlines()
#                                          if not re.search(r"(join\s+us|join\s+our|join\s+our\s+whatsapp)", l, re.I)]
#                         msg = "\n".join([l for l in cleaned_lines if l])
#                         # msg += ("\n\n-------------------------------------\n"
#                         #         "*Join us at:*\n"
#                         #         "WhatsApp: https://tinyurl.com/SuperDeals1dot0\n"
#                         #         "Telegram: https://t.me/superdeal1dot0")
                        
#                         send_to_channel(msg)
#                         send_to_whatsapp(msg)  # optional
                        
#                         row[5] = "SENT"
#                         recent_msgs.append(msg.lower())
#                         print("✅ Sent message updated to SENT status")
#                     changed = True
#                 updated_rows.append(row)
#             if changed:
#                 write_csv(header, updated_rows)
#             time.sleep(2)
#         except Exception as e:
#             print(f"⚠️ Error in sending worker: {e}")
#             time.sleep(3)

# # -------------------------
# # Run all workers
# # -------------------------
# if __name__ == "__main__":
#     threading.Thread(target=api_worker, daemon=True).start()
#     threading.Thread(target=sending_worker, daemon=True).start()
#     with client:
#         print("🚀 Orchestrator running (Telegram + API + WhatsApp + Channel)")
#         client.run_until_disconnected()

import os
import csv
import json
import time
import threading
import requests
import webbrowser
import pyautogui
import pygetwindow as gw
import pyperclip
import re
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
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
API_URL = "https://ekaro-api.affiliaters.in/api/converter/public"
CSV_FILE = "telegram_messages.csv"

# Validate critical configs
for key, val in {
    "API_ID": api_id, "API_HASH": api_hash, "API_KEY": API_KEY,
    "BOT_TOKEN": BOT_TOKEN, "CHANNEL_ID": CHANNEL_ID
}.items():
    if not val:
        raise EnvironmentError(f"❌ Missing required environment variable: {key}")

# Create CSV if missing
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
        try:
            with open(CSV_FILE, "r", newline='', encoding="utf-8") as f:
                return list(csv.reader(f))
        except Exception as e:
            print(f"⚠️ Error reading CSV: {e}")
            return [[]]

def write_csv(header, rows):
    with csv_lock:
        try:
            with open(CSV_FILE, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(rows)
        except Exception as e:
            print(f"⚠️ Error writing CSV: {e}")

def append_csv(row):
    with csv_lock:
        try:
            with open(CSV_FILE, "a", newline='', encoding="utf-8") as f:
                csv.writer(f).writerow(row)
        except Exception as e:
            print(f"⚠️ Error appending to CSV: {e}")

# -------------------------
# Telegram Worker (Monitor)
# -------------------------
client = TelegramClient('session_name', api_id, api_hash)
channels_to_monitor = get_joined_channel_ids()

@client.on(events.NewMessage(chats=channels_to_monitor))
async def handler(event):
    msg_text = (event.message.message or "").strip()
    if not msg_text:
        return
    msg_datetime = event.message.date.strftime("%Y-%m-%d %H:%M:%S")
    sender = await event.get_chat()
    username = getattr(sender, "username", None)
    message_id = event.message.id
    channel_link = f"https://t.me/{username}/{message_id}" if username else "N/A"
    append_csv([msg_datetime, channel_link, msg_text, "", "", "TBS"])
    print(f"📝 Queued message from Telegram: {msg_text[:60]}...")

# -------------------------
# API Worker
# -------------------------
def convert_message_via_api(message):
    payload = json.dumps({"deal": message, "convert_option": "convert_only"})
    headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
    try:
        response = requests.post(API_URL, headers=headers, data=payload, timeout=20)
        if response.status_code == 200:
            return response.json().get("data", "").strip()
        else:
            return f"API_ERROR: {response.text}"
    except Exception as e:
        return f"API_EXCEPTION: {e}"

def api_worker():
    while True:
        try:
            data = read_csv()
            if not data or len(data) < 2:
                time.sleep(2)
                continue
            header, rows = data[0], data[1:]
            changed = False
            updated_rows = []
            for row in rows:
                if len(row) < 6:
                    updated_rows.append(row)
                    continue
                if row[5] == "TBS":
                    print(f"🔄 Converting via API: {row[2][:60]}...")
                    updated_msg = convert_message_via_api(row[2])
                    if not updated_msg or "we could not find" in updated_msg.lower() or updated_msg.startswith("API_"):
                        row[4], row[5] = updated_msg, "ERROR"
                    else:
                        row[4], row[5] = updated_msg, "LU"
                    changed = True
                updated_rows.append(row)
            if changed:
                write_csv(header, updated_rows)
                print("✅ API updates saved to CSV")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Error in API worker: {e}")
            time.sleep(2)

# -------------------------
# WhatsApp Automation (optional)
# -------------------------
def restore_whatsapp_window():
    """
    Attempt to find a WhatsApp window and bring it to the front.
    Returns True if a window was found and activated, else False.
    """
    try:
        for window in gw.getWindowsWithTitle("WhatsApp"):
            try:
                if window.isMinimized:
                    window.restore()
                window.activate()
                window.maximize()
                # small click to focus message box area (if coordinate matches)
                #pyautogui.click(852, 1089) # LAptop
                pyautogui.click(779, 996) # Desktop

                return True
            except Exception:
                # continue trying other windows if activation fails
                continue
    except Exception as e:
        print(f"⚠️ restore_whatsapp_window error: {e}")
    return False

def is_whatsapp_web_open():
    try:
        return any("WhatsApp" in t or "web.whatsapp.com" in t for t in gw.getAllTitles())
    except Exception as e:
        print(f"⚠️ is_whatsapp_web_open error: {e}")
        return False

def WA_setup():
    try:
        if not is_whatsapp_web_open():
            webbrowser.open("https://web.whatsapp.com")
            print("⏳ Waiting for WhatsApp Web...")
            time.sleep(15)
        pyautogui.FAILSAFE = True
        # clicks to position focus in the browser (user may need to fine-tune)
        #pyautogui.click(49, 244) # Laptop
        pyautogui.click(x=28, y=233 )
        # Desktop
        time.sleep(0.5)
        #pyautogui.click(283, 284) # Laptop
        pyautogui.click(222, 240) # Desktop
        time.sleep(1)
    except Exception as e:
        print(f"⚠️ WA_setup error: {e}")

def send_to_whatsapp(msg, max_retries=100):
    """
    Try to send msg to WhatsApp using pyautogui.
    Returns True on success, False on failure after retries.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            WA_setup()
            restored = restore_whatsapp_window()
            if not restored:
                raise RuntimeError("WhatsApp window not found or couldn't be activated")

            print(f"📤 WA Attempt {attempt+1}: Sending message…")
            pyperclip.copy(msg)
            # click to ensure focus on input box (coordinates may need adjustment)
            #pyautogui.click(852, 1089)
            pyautogui.click(779, 996) # Desktop
            pyautogui.hotkey("ctrl", "v")
            time.sleep(1)
            pyautogui.press("enter")
            # small wait for UI to process send
            time.sleep(1)
            print("✅ WhatsApp sent successfully!")
            return True
        except Exception as e:
            print(f"❌ WhatsApp send failed (Attempt {attempt+1}): {e}")
            attempt += 1
            # small backoff
            time.sleep(5)
    print(f"🚨 WhatsApp failed after {max_retries} retries.")
    return False

# -------------------------
# Telegram Channel Poster
# -------------------------
def send_to_channel(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHANNEL_ID, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, data=payload, timeout=15)
        if response.status_code == 200:
            print("✅ Message sent to Telegram channel")
            return True
        else:
            print(f"❌ Failed to send to Telegram channel: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"⚠️ Telegram channel send error: {e}")
        return False

# -------------------------
# Sending Worker (LU messages)
# -------------------------
def sending_worker():
    recent_msgs = []
    while True:
        try:
            data = read_csv()
            if not data or len(data) < 2:
                time.sleep(1)
                continue
            header, rows = data[0], data[1:]
            changed = False
            updated_rows = []
            for row in rows:
                if len(row) < 6:
                    updated_rows.append(row)
                    continue
                if row[5] == "LU":
                    msg = (row[4] or "").strip()
                    # Basic validations
                    if not msg or msg.lower().startswith(("we could not locate", "api_")):
                        row[5] = "ERROR"
                        print("⚠️ Marked ERROR due to API/empty message")
                    elif msg.lower() in recent_msgs[-5:]:
                        row[5] = "DUPLICATE"
                        print("⚠️ Marked DUPLICATE (recent)")
                    else:
                        # Clean message (remove join us lines)
                        cleaned_lines = [l.strip() for l in msg.splitlines()
                                         if not re.search(r"(join\s+us|join\s+our|join\s+our\s+whatsapp)", l, re.I)]
                        cleaned_msg = "\n".join([l for l in cleaned_lines if l])

                        # Footer is DISABLED as requested (do not append signature)

                        # First: send to WhatsApp with retries
                        wa_success = send_to_whatsapp(cleaned_msg)

                        if not wa_success:
                            # After retries, if still failing -> mark WA_FAIL and DO NOT send to Telegram
                            row[5] = "WA_FAIL"
                            print("🚨 WA failed after retries. Not sending to Telegram.")
                        else:
                            # WA success -> proceed to Telegram
                            tg_success = send_to_channel(cleaned_msg)
                            if tg_success:
                                row[5] = "SENT"
                                recent_msgs.append(cleaned_msg.lower())
                                print("✅ Message marked SENT")
                            else:
                                # Telegram failed but WA succeeded — choose behavior: mark TG_FAIL
                                # Here we mark TG_FAIL so you can re-process later if desired
                                row[5] = "TG_FAIL"
                                print("⚠️ Telegram send failed, but WhatsApp succeeded. Marked TG_FAIL.")
                    changed = True
                updated_rows.append(row)
            if changed:
                write_csv(header, updated_rows)
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Error in sending worker: {e}")
            time.sleep(1)

# -------------------------
# Run all workers
# -------------------------
if __name__ == "__main__":
    threading.Thread(target=api_worker, daemon=True).start()
    threading.Thread(target=sending_worker, daemon=True).start()
    with client:
        print("🚀 Orchestrator running (Telegram + API + WhatsApp + Channel)")
        client.run_until_disconnected()
