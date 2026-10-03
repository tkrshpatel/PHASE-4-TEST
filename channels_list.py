from telethon.sync import TelegramClient
from telethon.tl.types import Channel
from dotenv import load_dotenv
import os   

load_dotenv()

# Replace with your actual credentials
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
if not api_id or not api_hash:
    raise ValueError("API_ID and API_HASH must be set in the environment variables.")

# your own channel username (to skip)
EXCLUDE_CHANNEL = "@superdeal1dot0"

def get_joined_channel_ids(session_name='session_name'):
    client = TelegramClient(session_name, api_id, api_hash)

    channel_ids = []
    with client:
        for dialog in client.iter_dialogs():
            if isinstance(dialog.entity, Channel) and dialog.is_channel:
                # Exclude your own channel by username
                username = getattr(dialog.entity, "username", "")
                if username and f"@{username.lower()}" == EXCLUDE_CHANNEL.lower():
                    continue
                channel_ids.append(dialog.entity.id)
    
    return channel_ids
