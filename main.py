from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from utils import loadConfiguration, getConfigFileVariable
import tuya
import os
import datetime

EMOJI_LUCE_ACCESA = "\U0001F31E"
EMOJI_LUCE_SPENTA = "\U0001F31A"
EMOJI_FOTO = "\U0001F4F8"
EMOJI_VIDEO = "\U0001F3A5"

async def default_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello \U0001F643 {update.effective_user.first_name}')

async def accendiLuce(update: Update, context: ContextTypes.DEFAULT_TYPE, cancellaMessaggio = False) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}" ):
        return await default_message_handler(update, context)
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
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}" ):
        return await default_message_handler(update, context)
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
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}" ):
        return await default_message_handler(update, context)
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
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}" ):
        return await default_message_handler(update, context)
    try:
        k = await context.bot.send_message(update.message.chat_id, "Recupero del file in corso...")
        f = open("logBot.txt", "rb")
        await context.bot.send_document(chat_id=update.message.chat_id, document=f, caption="logBot")
        f.close()
        await context.bot.delete_message(chat_id=k.chat_id, message_id=k.message_id)
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')

async def getPic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}" ):
        return await default_message_handler(update, context)
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
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}" ):
        return await default_message_handler(update, context)
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
        [InlineKeyboardButton(f"{EMOJI_LUCE_ACCESA} Accendi la luce", callback_data="command:accendi"), InlineKeyboardButton(f"{EMOJI_LUCE_SPENTA} Spegni la luce", callback_data="command:spegni")],
        [InlineKeyboardButton(f"{EMOJI_FOTO} Foto", callback_data="command:foto"), InlineKeyboardButton(f"{EMOJI_VIDEO} Video", callback_data="command:video")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Azioni disponibili', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    if "command:accendi" in data:
        return await accendiLuce(query, context, True)
    elif "command:spegni" in data:
        return await spegniLuce(query, context, True)
    elif "command:foto" in data:
        return await getPic(query, context)
    elif "command:video" in data:
        return await getRec(query, context)
    #await query.edit_message_text(text=f"Azione non definita")
    await query.edit_message_text(text=f"Azione non definita")

async def printToken(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}" ):
        return await default_message_handler(update, context)
    try:
        k = await context.bot.send_message(update.message.chat_id, "Leggo il token dal file...")
        config = loadConfiguration()
        await context.bot.edit_message_text(f'Il token letto dal file è {config["access_token"]}', chat_id=update.message.chat_id, message_id=k.message_id)
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')

async def getConfigFile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}" ):
        return await default_message_handler(update, context)
    try:
        k = await context.bot.send_message(update.message.chat_id, "Recupero del file di configurazione in corso...")
        fileName = getConfigFileVariable() 
        f = open(f"{fileName}", "rb")
        await context.bot.send_chat_action(chat_id=k.chat_id, action = "upload_document")
        await context.bot.sendDocument(chat_id=k.chat_id, document=f, filename=f"{fileName}")
        f.close()
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')

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
app.add_handler(CommandHandler("printtoken", printToken))
app.add_handler(CommandHandler("getconfigfile", getConfigFile))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, default_message_handler))

# Error handler
#app.add_error_handler(error_handler)

try:
    app.run_polling()
except Exception as e:
    f = open("logBot.txt", "a+")
    print(f'Errore: {repr(e)}', file=f)
    f.close()