from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import subprocess
from threading import Thread
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from utils import loadConfiguration, getConfigFileVariable
import tuya
import os
import time
import datetime
import emojis
import io
import matplotlib.pyplot as plt
from datetime import datetime


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


def capture_photo():
    cmd = ['raspistill', '-t', '1000', '-o', '-']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    photo_data = process.stdout.read()
    process.wait()
    return photo_data


async def getPic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = loadConfiguration()
    if (f"{update.message.chat_id}" != f"{config['chat_id_admin']}"):
        return await default_message_handler(update, context)
    try:
        k = await context.bot.send_message(update.message.chat_id, "Sto scattando una foto...")
        dis(["Cheeeese!"])
        now = datetime.now()
        filename = now.strftime("%Y%m%d%H%M%S")
        filename = f"{filename}.png"
        # os.system(
        #   f"raspistill -w 1000 -h 1000 -t 2000 -n -dt -e png -o {filename}")
        photo = capture_photo()
        dis(["Foto fatta!"])
        # f = open(filename, "rb")
        await context.bot.send_chat_action(chat_id=k.chat_id, action="upload_photo")
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo, caption=f"{filename}")
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
        now = datetime.now()
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
                              callback_data="command:humidityTemperature")],
        [InlineKeyboardButton(
            f"{emojis.CHART_INCREASING} Grafico umidità e temperatura {emojis.CHART_DECREASING}", callback_data="command:getchart")]
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
    elif "command:getchart" in data:
        return await getchart(query, context)
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
    when = datetime.fromtimestamp(int(lastValue["timestamp"])/1000.0)
    when = when.strftime('%d/%m/%Y %H:%M:%S')
    msg = f'{emojis.MANTELPIECE_CLOCK} {when} {emojis.DROPLET}{lastValue["humidity"]}% {emojis.THERMOMETER}{lastValue["temperature"]}°'
    global bot
    await bot.set_my_short_description(f"{msg}")
    return await update.message.reply_text(msg)


def createChart():
    daily_data = {}

    with (open("/home/pi/temperature.csv", "r")) as f:
        allLines = f.readlines()
        allLines.reverse()
        for l in allLines:
            l = l.strip()
            l = l.replace("\x00", "")
            if len(l) < 1:
                continue
            values = l.split(",")
            temperature = float(values[0])
            humidity_value = float(values[2])
            timestamp_ms = int(values[1])

            timestamp_sec = timestamp_ms / 1000.0
            date_object = datetime.fromtimestamp(timestamp_sec)
            date_only = date_object.date()

            if date_only in daily_data:
                # If the date already exists, update the daily values
                daily_data[date_only]['temperature'].append(temperature)
                daily_data[date_only]['humidity'].append(humidity_value)
            else:
                # If the date doesn't exist, create a new entry
                daily_data[date_only] = {
                    'temperature': [temperature],
                    'humidity': [humidity_value]
                }

    daily_averages = {}
    xValues = []
    yTemp = []
    yHum = []
    for date, data in daily_data.items():
        avg_temperature = sum(data['temperature']) / len(data['temperature'])
        avg_humidity = sum(data['humidity']) / len(data['humidity'])
        daily_averages[date] = {
            'average_temperature': avg_temperature,
            'average_humidity': avg_humidity
        }
        xValues.append(date)
        yTemp.append(int(avg_temperature))
        yHum.append(int(avg_humidity))
    maxTemp = max(yTemp)
    maxTemp = int(maxTemp)
    maxHum = max(yHum)
    maxHum = int(maxHum)

    minTemp = min(yTemp)
    minTemp = int(minTemp)
    minHum = min(yHum)
    minHum = int(minHum)

    plt.figure(figsize=(20, 12))  # Set the figure size (adjust as needed)

    plt.plot(xValues, yTemp, label='Temperature')
    plt.plot(xValues, yHum, label='Humidity')

    textPosition = len(xValues)/2 + len(xValues)/4
    # print(f'{textPosition}')

    textPosition = xValues[int(textPosition)]

    plt.axhline(maxTemp, color='red', linestyle='--',
                label=f'Max temperature {maxTemp}')

    plt.text(textPosition, maxTemp, f'Max temperature = {maxTemp}°C', color='red',
             fontsize=10, ha='right', va='bottom')

    plt.axhline(minTemp, color='darkorange', linestyle='--',
                label=f'Min temperature {minTemp}')

    plt.text(textPosition, minTemp, f'Min temperature = {minTemp}°C', color='darkorange',
             fontsize=10, ha='right', va='bottom')

    plt.axhline(maxHum, color='blue', linestyle='--',
                label=f'Max humidity {maxHum}')

    plt.text(textPosition, maxHum, f'Max humidity = {maxHum}%', color='blue',
             fontsize=10, ha='right', va='bottom')

    plt.axhline(minHum, color='deepskyblue', linestyle='--',
                label=f'Min humidity {minHum}')

    plt.text(textPosition, minHum, f'Min humidity = {minHum}%', color='deepskyblue',
             fontsize=10, ha='right', va='bottom')

    plt.xlabel('Time')
    plt.ylabel('Temperature and Humidity')
    plt.title('Temperature and Humidity over time')
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plt.close()

    return buf


async def getchart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    k = await context.bot.send_message(update.message.chat_id, "Sto creando il grafico...")
    chart_buff = createChart()
    await context.bot.send_chat_action(chat_id=k.chat_id, action="upload_photo")
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=chart_buff)
    await context.bot.delete_message(chat_id=k.chat_id, message_id=k.message_id)


async def setDescriptionWithInformation():
    global bot
    import noderedconnector
    lastValue = noderedconnector.readLastValue()
    when = datetime.fromtimestamp(int(lastValue["timestamp"])/1000.0)
    when = when.strftime('%d/%m/%Y %H:%M:%S')
    if (lastValue is None):
        await bot.set_my_short_description(f"{when} Nessun dato...")
    msg = f'{emojis.MANTELPIECE_CLOCK} {when} {emojis.DROPLET}{lastValue["humidity"]}% {emojis.THERMOMETER}{lastValue["temperature"]}°'
    await bot.set_my_short_description(f"{msg}")

config = loadConfiguration()
global bot
bot = telegram.Bot(config["bot_token"])

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
app.add_handler(CommandHandler("readht", readHT))
app.add_handler(CommandHandler("adminpanel", adminPanel))
app.add_handler(CommandHandler("startnodered", startNodeRedServer))
app.add_handler(CommandHandler("stopnodered", stopNodeRedServer))


app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND, default_message_handler))

# Error handler
# app.add_error_handler(error_handler)

scheduler = AsyncIOScheduler()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)
job = scheduler.add_job(setDescriptionWithInformation, 'interval', seconds=60)
scheduler.start()

try:
    f = open("logBot.txt", "a+")
    print('Bot avviato con successo', file=f)
    f.close()
    os.system("node-red-start &")
    app.run_polling()
except Exception as e:
    f = open("logBot.txt", "a+")
    print(f'Errore: {repr(e)}', file=f)
    f.close()
