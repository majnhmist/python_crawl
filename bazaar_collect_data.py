from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import json

async def at_update_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    old_data = {}
    while True:
        try:
            data = {'query': 'get_recent', 'selector': 100}
            response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=30)
            json_response = response.content.decode("utf-8", "ignore")#json_response = json => dict
            json_response = json.loads(json_response)
            data_api = json_response["data"]
            if old_data["first_seen"] != data_api[0]["first_seen"] or len(old_data) == 0:
                await update.message.reply_text(data_api[0]["first_seen"])
                old_data["first_seen"] = data_api[0]["first_seen"]
            print(old_data["first_seen"],' ',data_api[0]["first_seen"])
        except:
            print("dang co loi xay ra . . .")

app = ApplicationBuilder().token("6469651267:AAGu9sqF0txguW0uoKUZUNQlgTmuTp4kcL8").build()
app.add_handler(CommandHandler("at_update_data", at_update_data))
app.run_polling()