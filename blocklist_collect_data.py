import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def at_update_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    check = []
    while True:
        try:
            links  = []
            url = 'https://www.blocklist.de/en/export.html'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            datas = soup.find_all('a', title="all Atacker-IP's from the last 48 Hours")
            for data in datas:
                link = data.get('href')
                links.append(link)
            if check != links or len(check) == 0:
                await update.message.reply_text("NEWS: all Atacker-IP's from the last 48 Hours")
                for link in links:
                    await update.message.reply_text(link)
                check = links
        except:
            print("dang co loi xay ra . . .")

app = ApplicationBuilder().token("6469651267:AAGu9sqF0txguW0uoKUZUNQlgTmuTp4kcL8").build()
app.add_handler(CommandHandler("at_update_data", at_update_data))
app.run_polling()