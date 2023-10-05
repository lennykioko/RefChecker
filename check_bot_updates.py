import os
import requests

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("APP_TG_TOKEN")

api_url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    if data['ok']:
        latest_update = data['result'][-1]

        chat_id = latest_update['message']['chat']['id']

        print("Chat ID:", chat_id)
    else:
        print("Error in the response data.")
else:
    print("Error in the API request.")
