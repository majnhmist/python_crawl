from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import json
from bs4 import BeautifulSoup

async def AUD(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    old_data_bazaar = {}
    old_data_vxvault = []
    old_data_blocklist = []
    while True:
        try:
            #bazaar
            data = {'query': 'get_recent', 'selector': 100}
            response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=30)
            json_response = response.content.decode("utf-8", "ignore")#json_response = json => dict
            json_response = json.loads(json_response)
            data_api = json_response["data"]
            if len(old_data_bazaar) == 0 or (old_data_bazaar["first_seen"] != data_api[0]["first_seen"]):
                Signature = data_api[0]["signature"]
                await update.message.reply_text(f'NEWS of Bazaar.abuse.ch:\nDate (UTC): {data_api[0]["first_seen"]}\nSHA256 hash: {data_api[0]["sha256_hash"]}\nType: {data_api[0]["file_type"]}\nSignature: {Signature}\nTag: {data_api[0]["tags"]}\nReporter: {data_api[0]["reporter"]}')
                old_data_bazaar["first_seen"] = data_api[0]["first_seen"]
            #blocklist
            links  = []
            url = 'https://www.blocklist.de/en/export.html'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            datas = soup.find_all('a', title="all Atacker-IP's from the last 48 Hours")
            message = ""
            for data in datas:
                link = data.get('href')
                message = message + link + '\n'
                links.append(link)
            if old_data_blocklist != links or len(old_data_blocklist) == 0:
                message = "NEWS of blocklist.de : all Atacker-IP's from the last 48 Hours\n" + message 
                await update.message.reply_text(message)
                old_data_blocklist = links
            #vxvault
            url = 'http://vxvault.net/ViriList.php?s=0&m=40'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('div', id = 'page')
            rows = table.find_all('tr')
            colums = rows[1].find_all('td')
            message = "NEWS of vxvault.net:\n"
            message = message + "Data: " + colums[0].text.strip() + '\n'
            message = message + "URL: " + colums[1].text.strip() + '\n'
            message = message + "MD5: " + colums[2].text.strip() + '\n'
            message = message + "IP: " + colums[3].text.strip() + '\n'
            message = message + "Tools: " + colums[4].text.strip() + '\n'
            if old_data_vxvault != colums or len(old_data_vxvault) == 0:
                await update.message.reply_text(message)
                old_data_vxvault = colums
        except:
            print("dang co loi xay ra . . .")

app = ApplicationBuilder().token("6469651267:AAGu9sqF0txguW0uoKUZUNQlgTmuTp4kcL8").build()
app.add_handler(CommandHandler("AUD", AUD))
app.run_polling()