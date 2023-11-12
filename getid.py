from telethon.sync import TelegramClient

api_id = '16050166'
api_hash = 'de31ddc2d7951901c7aa1ab0b93d0b4a'

with TelegramClient('anon', api_id, api_hash) as client:
    entity = client.get_entity('Aris_4j4')  # Replace 'username' with the username of the chat
    print(entity.id)
