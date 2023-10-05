import requests

TOKEN = "1006615027:AAHGxcvNkET_rMwfcj3ZQ0Zibg1ACGAtFDY"

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
