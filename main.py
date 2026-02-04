import requests
import json
import time

BOT_TOKEN = "8512497270:AAE6LZAZJ5qV-FQZU74Y8YbNyZYEoZElNxQ"
PHONE_LOOKUP_API = "https://anishexploits.site/anish-exploits/api.php?key=demo-testing&num="

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

offset = 0

def get_updates(offset):
    url = API_URL + "getUpdates"
    params = {"timeout": 30, "offset": offset}
    return requests.get(url, params=params).json()

def send_message(chat_id, text, reply_markup=None, parse_mode=None):
    url = API_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}

    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    if parse_mode:
        data["parse_mode"] = parse_mode

    requests.post(url, data=data)

def phone_lookup(number):
    try:
        response = requests.get(PHONE_LOOKUP_API + number, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

print("Bot is running...")

while True:
    try:
        updates = get_updates(offset)

        for update in updates.get("result", []):
            offset = update["update_id"] + 1

            message = update.get("message")
            if not message or "text" not in message:
                continue

            chat_id = message["chat"]["id"]
            text = message["text"].strip()

            if text == "/start":
                keyboard = {
                    "keyboard": [[{"text": "📱 Phone Lookup"}]],
                    "resize_keyboard": True
                }
                send_message(chat_id, "👋 Welcome!\nChoose an option:", reply_markup=keyboard)

            elif text == "📱 Phone Lookup":
                send_message(chat_id, "📞 Send 10 digit mobile number:")

            elif text.isdigit() and len(text) == 10:
                send_message(chat_id, "🔍 Looking up number...")
                data = phone_lookup(text)
                formatted = json.dumps(data, indent=2)
                send_message(chat_id, f"<pre>{formatted}</pre>", parse_mode="HTML")

            else:
                send_message(chat_id, "❌ Invalid input. Send a 10 digit mobile number.")

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
