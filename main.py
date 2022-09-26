from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from utils import loadConfiguration
import tuya
import os
import datetime

async def default_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        config = loadConfiguration()
        await context.bot.send_message(chat_id=config["chat_id_admin"], text="Errore error_handler")
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')

async def accendiLuce(update: Update, context: ContextTypes.DEFAULT_TYPE, cancellaMessaggio = False) -> None:
    try:
        k = await context.bot.send_message(update.message.chat_id, "Accensione della luce in corso...")
        t = tuya.turnOn()
        msg = ""
        if t:
            msg = "Luce accesa"
        else:
            msg = "Impossibile accendere la luce"
        m = await context.bot.edit_message_text(f'{msg}', chat_id=update.message.chat_id, message_id=k.message_id)
        if cancellaMessaggio == True:
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=m.message_id)
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')

async def spegniLuce(update: Update, context: ContextTypes.DEFAULT_TYPE, cancellaMessaggio = False) -> None:
    try:
        k = await context.bot.send_message(update.message.chat_id, "Spegnimento della luce in corso...")
        t = tuya.turnOff()
        msg = ""
        if t:
            msg = "Luce spenta"
        else:
            msg = "Impossibile spegnere la luce"
        m = await context.bot.edit_message_text(f'{msg}', chat_id=update.message.chat_id, message_id=k.message_id)
        if cancellaMessaggio == True:
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=m.message_id)
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

async def getPic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        k = await context.bot.send_message(update.message.chat_id, "Sto scattando una foto...")
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d%H%M%S")
        filename = f"{filename}.png"
        os.system(f"raspistill -w 1000 -h 1000 -t 2000 -n -dt -e png -o {filename}")
        f = open(filename, "rb")
        await context.bot.send_chat_action(chat_id=k.chat_id, action = "upload_photo")
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=f, caption=f"{filename}")
        f.close()
        await context.bot.delete_message(chat_id=k.chat_id, message_id=k.message_id)
        os.system(f"rm {filename}")
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')

async def getRec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        k = await context.bot.send_message(update.message.chat_id, "Sto registrando un video...")
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d%H%M%S")
        video = f"{filename}.h264"
        filename = f"{filename}.mp4"
        os.system("raspivid -t 5000 -n -o {}".format(video))
        os.system("MP4Box -add {} -fps 30 {}".format(video, filename))
        f = open(filename, "rb")
        await context.bot.send_chat_action(chat_id=k.chat_id, action = "upload_video")
        await context.bot.send_video(chat_id=update.message.chat_id, video=f, caption=f"{filename}")
        f.close()
        await context.bot.delete_message(chat_id=k.chat_id, message_id=k.message_id)
        os.system(f"rm {filename}")
        os.system(f"rm {video}")
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')

async def keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Accendi la luce", callback_data="command:accendi"), InlineKeyboardButton("Spegni la luce", callback_data="command:spegni")],
        [InlineKeyboardButton("Foto", callback_data="command:foto"), InlineKeyboardButton("Video", callback_data="command:video")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Azioni disponibili', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if "command:" in query.data:
        match query.data:
            case "command:accendi":
                return await accendiLuce(query, context, True)
            case "command:spegni":
                return await spegniLuce(query, context, True)
            case "command:foto":
                return await getPic(query, context)
            case "command:video":
                return await getRec(query, context)
        #await query.edit_message_text(text=f"Azione non definita")
    await query.edit_message_text(text=f"Azione non definita")


config = loadConfiguration()
app = ApplicationBuilder().token(config["bot_token"]).build()



# Setto gli handler
app.add_handler(CallbackQueryHandler(button))

app.add_handler(CommandHandler("accendiluce", accendiLuce))
app.add_handler(CommandHandler("spegniluce", spegniLuce))
app.add_handler(CommandHandler("newtoken", newToken))
app.add_handler(CommandHandler("getlogfile", getLogFile))
app.add_handler(CommandHandler("getpic", getPic))
app.add_handler(CommandHandler("getrec", getRec))
app.add_handler(CommandHandler("keyboard", keyboard))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, default_message_handler))


# Error handler
#app.add_error_handler(error_handler)

try:
    app.run_polling()
except Exception as e:
    f = open("logBot.txt", "a+")
    print(f'Errore: {repr(e)}', file=f)
    f.close()