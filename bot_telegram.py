from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    a = []
    a.append("le")
    a.append("duc")
    a.append("manh")
    message = ""
    for i in a:
        message = message + i + '\n'
    await update.message.reply_text(message)

app = ApplicationBuilder().token("6469651267:AAGu9sqF0txguW0uoKUZUNQlgTmuTp4kcL8").build()
app.add_handler(CommandHandler("hello", hello))
app.run_polling()
