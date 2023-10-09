import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def at_update_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    check = []
    while True:
        try:
            url = 'http://vxvault.net/ViriList.php?s=0&m=40'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('div', id = 'page')
            rows = table.find_all('tr')
            colums = rows[1].find_all('td')
            if check != colums or len(check) == 0:
                await update.message.reply_text("NEWS of vxvault.net")
                await update.message.reply_text(f"{colums[0].text.strip()}  {colums[1].text.strip()}  {colums[2].text.strip()}  {colums[3].text.strip()}  {colums[4].text.strip()}")
                check = colums
        except:
            print("dang co loi xay ra . . .")

app = ApplicationBuilder().token("6469651267:AAGu9sqF0txguW0uoKUZUNQlgTmuTp4kcL8").build()
app.add_handler(CommandHandler("at_update_data", at_update_data))
app.run_polling()