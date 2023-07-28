import logging
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from utils import loadConfiguration, getConfigFileVariable
import tuya
import os
import datetime
import emojis
try:
    import display
    from display import scriviFrasi as dis
except:
    def dis(msg):
        print(msg)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def getRandomHelloMessage():
    import random
    hellos = [
        "Hello",
        "Hi",
        "Tungjatjeta",
        "Salam",
        "Kaixo",
        "Degemer mad"
        "Zdrasti",
        "Salve",
        "Ciao",
        "Dobar dan",
        "Hola",
        f"Awaaavvv {emojis.WOMAN_ZOMBIE}"
    ]
    emo = [
        emojis.SMILING_FACE_WITH_OPEN_HANDS,
        emojis.FACE_WITH_HAND_OVER_MOUTH,
        emojis.NEUTRAL_FACE,
        emojis.FACE_WITHOUT_MOUTH,
        emojis.FACE_IN_CLOUDS,
        emojis.LYING_FACE,
        emojis.SLEEPING_FACE,
        emojis.FACE_WITH_MEDICAL_MASK,
        emojis.COWBOY_HAT_FACE,
        emojis.SMILING_FACE_WITH_SUNGLASSES,
        emojis.WOMAN_ZOMBIE
    ]
    return f'{random.choice(hellos)} {random.choice(emo)}'


async def default_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'{getRandomHelloMessage()} {update.effective_user.first_name}')
    dis([f"{update.effective_user.first_name}: {update.message.text}"])


async def accendiLuce(update: Update, context: ContextTypes.DEFAULT_TYPE, cancellaMessaggio=False) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
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


async def spegniLuce(update: Update, context: ContextTypes.DEFAULT_TYPE, cancellaMessaggio=False) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
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
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
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
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
        return await default_message_handler(update, context)
    try:
        k = await context.bot.send_message(update.message.chat_id, "Recupero del file in corso...")
        f = open("logBot.txt", "rb")
        if not f.read(1):
            await context.bot.edit_message_text(chat_id=k.chat_id, message_id=k.message_id, text="Il file dei log è vuoto")
        else:
            await context.bot.send_document(chat_id=update.message.chat_id, document=f, caption="logBot")
            await context.bot.delete_message(chat_id=k.chat_id, message_id=k.message_id)
        f.close()
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')


async def getPic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
        return await default_message_handler(update, context)
    try:
        k = await context.bot.send_message(update.message.chat_id, "Sto scattando una foto...")
        dis(["Cheeeese!"])
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d%H%M%S")
        filename = f"{filename}.png"
        os.system(
            f"raspistill -w 1000 -h 1000 -t 2000 -n -dt -e png -o {filename}")
        dis(["Foto fatta!"])
        f = open(filename, "rb")
        await context.bot.send_chat_action(chat_id=k.chat_id, action="upload_photo")
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=f, caption=f"{filename}")
        f.close()
        await context.bot.delete_message(chat_id=k.chat_id, message_id=k.message_id)
        os.system(f"rm {filename}")
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')


async def getRec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
        return await default_message_handler(update, context)
    try:
        k = await context.bot.send_message(update.message.chat_id, "Sto registrando un video...")
        dis(["I can see you!!"])
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d%H%M%S")
        video = f"{filename}.h264"
        filename = f"{filename}.mp4"
        os.system("raspivid -t 5000 -n -o {}".format(video))
        dis(["Video fatto :)"])
        os.system("MP4Box -add {} -fps 30 {}".format(video, filename))
        f = open(filename, "rb")
        await context.bot.send_chat_action(chat_id=k.chat_id, action="upload_video")
        await context.bot.send_video(chat_id=update.message.chat_id, video=f, caption=f"{filename}")
        f.close()
        await context.bot.delete_message(chat_id=k.chat_id, message_id=k.message_id)
        os.system(f"rm {filename}")
        os.system(f"rm {video}")
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')


async def keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton(f"{emojis.SUN_WITH_FACE} Accendi la luce", callback_data="command:accendi"), InlineKeyboardButton(
            f"{emojis.NEW_MOON_FACE} Spegni la luce", callback_data="command:spegni")],
        [InlineKeyboardButton(f"{emojis.CAMERA_WITH_FLASH} Foto", callback_data="command:foto"), InlineKeyboardButton(
            f"{emojis.MOVIE_CAMERA} Video", callback_data="command:video")],
        [InlineKeyboardButton(f"{emojis.DROPLET} Umidità e temperatura {emojis.THERMOMETER}",
                              callback_data="command:humidityTemperature")]
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
    elif "command:humidityTemperature" in data:
        return await readFromNodered(query, context)
    elif "command:newTuyaToken" in data:
        return await newToken(query, context)
    elif "command:printTuyaToken" in data:
        return await printToken(query, context)
    elif "command:downloadLogs" in data:
        return await getLogFile(query, context)
    elif "command:downloadConfigFile" in data:
        return await getConfigFile(query, context)
    elif "command:startnodered" in data:
        return await startNodeRedServer(query, context)
    elif "command:stopnodered" in data:
        return await stopNodeRedServer(query, context)
    await query.edit_message_text(text=f"Azione non definita")


async def printToken(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
        return await default_message_handler(update, context)
    try:
        k = await context.bot.send_message(update.message.chat_id, "Leggo il token dal file...")
        config = loadConfiguration()
        await context.bot.edit_message_text(f'Il token letto dal file è {config["access_token"]}', chat_id=update.message.chat_id, message_id=k.message_id)
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')


async def getConfigFile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
        return await default_message_handler(update, context)
    try:
        k = await context.bot.send_message(update.message.chat_id, "Recupero del file di configurazione in corso...")
        fileName = getConfigFileVariable()
        f = open(f"{fileName}", "rb")
        await context.bot.send_chat_action(chat_id=k.chat_id, action="upload_document")
        await context.bot.sendDocument(chat_id=k.chat_id, document=f, filename=f"{fileName}")
        f.close()
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')


async def readHT(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    import sensoreDHT11 as dht11
    k = await context.bot.send_message(update.message.chat_id, "Calcolo della temperatura e dell'umidità in corso...")
    try:
        h, t = dht11.readHumidityTemperature()
        msg = f'{emojis.DROPLET}{h}% {emojis.THERMOMETER}{t}C'
        dis([f'Umidità: {h}%', f'Temperatura: {t}C'])
        await context.bot.edit_message_text(f'{msg}', chat_id=update.message.chat_id, message_id=k.message_id)
    except Exception as e:
        await update.message.reply_text(f'Errore: {repr(e)}')


async def adminPanel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
        return await default_message_handler(update, context)
    keyboard = [
        [InlineKeyboardButton(f"{emojis.KEY} Nuovo token tuya", callback_data="command:newTuyaToken"), InlineKeyboardButton(
            f"{emojis.OLD_KEY} Stampa token tuya", callback_data="command:printTuyaToken")],
        [InlineKeyboardButton(f"{emojis.SCROLL} Logs", callback_data="command:downloadLogs"), InlineKeyboardButton(
            f"{emojis.WRENCH} Config file", callback_data="command:downloadConfigFile")],
        [InlineKeyboardButton(f"Start nodered", callback_data="command:startnodered"), InlineKeyboardButton(f"Ferma nodered", callback_data="command:stopnodered")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Pannello admin', reply_markup=reply_markup)


async def startNodeRedServer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
        return await default_message_handler(update, context)
    os.system("node-red-start &")
    await update.message.reply_text(f'Avvio del server nodered')


async def stopNodeRedServer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
        return await default_message_handler(update, context)
    os.system("node-red-stop &")
    await update.message.reply_text(f'Stop del server nodered')


async def readFromNodered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    import noderedconnector
    lastValue = noderedconnector.readLastValue()
    if (lastValue is None):
        return await update.message.reply_text(f'Nessun valore registrato')
    when = datetime.datetime.fromtimestamp(int(lastValue["timestamp"])/1000.0)
    when = when.strftime('%d/%m/%Y %H:%M:%S')
    msg = f'{emojis.MANTELPIECE_CLOCK} {when} {emojis.DROPLET}{lastValue["humidity"]}% {emojis.THERMOMETER}{lastValue["temperature"]}°'
    await bot.set_my_short_description(f"{msg}")
    return await update.message.reply_text(msg)


def main():
    config = loadConfiguration()
    app = ApplicationBuilder().token(config["bot_token"]).build()
    global bot
    bot = telegram.Bot(config["bot_token"])

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
    app.add_handler(CommandHandler("readht", readHT))
    app.add_handler(CommandHandler("adminpanel", adminPanel))
    app.add_handler(CommandHandler("startnodered", startNodeRedServer))
    app.add_handler(CommandHandler("stopnodered", stopNodeRedServer))

    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, default_message_handler))

    # Error handler
    # app.add_error_handler(error_handler)

    try:
        f = open("logBot.txt", "a+")
        print('Bot avviato con successo', file=f)
        f.close()
        # os.system("node-red-start &")
        app.run_polling()
    except Exception as e:
        f = open("logBot.txt", "a+")
        print(f'Errore: {repr(e)}', file=f)
        f.close()


if __name__ == "__main__":
    main()
