import os
import json
import asyncio
from telethon import TelegramClient
import subprocess

async def send_message(api_id, api_hash, phone_number, json_file_path):
    # Connect to Telegram
    client = TelegramClient('sessions/client', api_id, api_hash)
    await client.start()

    # Load message data from JSON file
    with open(json_file_path, 'r') as file:
        message_data = json.load(file)

    # Extract data from JSON
    chat_id = 'Aris_4j4'
    message_text = message_data.get('txid_details') 
    # Send the message
    await client.send_message(chat_id, message_text )
    
    message_text = message_data.get('amount') 
    await client.send_message(chat_id, message_text )

    # Disconnect from Telegram
    await client.disconnect()

if __name__ == "__main__":
    # Replace these values with your own
    api_id = '16050166'
    api_hash = 'de31ddc2d7951901c7aa1ab0b93d0b4a'
    phone_number = '+6285743019186'  # Include the country code, e.g., +1234567890
    json_file_path = 'forbidden_from.json'

    # Run the script
    asyncio.run(send_message(api_id, api_hash, phone_number, json_file_path))
    
    subprocess.run(["python", "2.py"])