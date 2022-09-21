from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import json
from utils import loadConfiguration
import tuya

async def default_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def accendiLuce(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        k = await context.bot.send_message(update.message.chat_id, "Accensione della luce in corso...")
        t = tuya.turnOn()
        msg = ""
        if t:
            msg = "Luce accesa"
        else:
            msg = "Impossibile accendere la luce"
        await context.bot.edit_message_text(f'{msg}', chat_id=update.message.chat_id, message_id=k.message_id)
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')

async def spegniLuce(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        k = await context.bot.send_message(update.message.chat_id, "Spegnimento della luce in corso...")
        t = tuya.turnOff()
        msg = ""
        if t:
            msg = "Luce spenta"
        else:
            msg = "Impossibile spegnere la luce"
        await context.bot.edit_message_text(f'{msg}', chat_id=update.message.chat_id, message_id=k.message_id)
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')

async def newToken(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        k = await context.bot.send_message(update.message.chat_id, "Richiesta del token in corso...")
        t, token = tuya.getNewToken()
        msg = ""
        if t:
            msg = f"Token ricevuto con successo: {token}"
        else:
            msg = "Impossibile richiedere un nuovo token"
        await context.bot.edit_message_text(f'{msg}', chat_id=update.message.chat_id, message_id=k.message_id)
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')

async def getLogFile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        k = await context.bot.send_message(update.message.chat_id, "Recupero del file in corso...")
        f = open("logBot.txt", "rb")
        await context.bot.send_document(chat_id=update.message.chat_id, document=f, caption="logBot")
        f.close()
        await context.bot.delete_message(chat_id=k.chat_id, message_id=k.message_id)
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')


config = loadConfiguration()
app = ApplicationBuilder().token(config["bot_token"]).build()

# Setto gli handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, default_message_handler))
app.add_handler(CommandHandler("accendiluce", accendiLuce))
app.add_handler(CommandHandler("spegniluce", spegniLuce))
app.add_handler(CommandHandler("newtoken", newToken))
app.add_handler(CommandHandler("getlogfile", getLogFile))

try:
    app.run_polling()
except Exception as e:
    f = open("logBot.txt", "a+")
    print(f'Errore: {repr(e)}', file=f)
    f.close()