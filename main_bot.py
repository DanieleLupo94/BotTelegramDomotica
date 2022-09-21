import utelegram
import json
import tuya_micropython as tuya
from logger import log

CONFIG_FILE = "config.json"

def loadConfiguration():
    return json.load(open(CONFIG_FILE, "a+"))

def default_message_handler(message):
    log(f"Mi ha scritto {message['message']['chat']['id']}")
    bot.send(message['message']['chat']['id'], f"Ti ho letto {message}")

def getDevices(message):
    log(f"Recupero i dispositivi per {message['message']['chat']['id']}")
    message = bot.sendAndGetMessage(message['message']['chat']['id'], "Recupero i dispositivi")
    msg = ""
    try:
        d = tuya.getDevices()
        msg = f"{d}"
    except Exception as e:
        msg = f"Errore: {repr(e)}"
    log(f"Rispondo a {message['chat']['id'], message['message_id']} con {msg}")
    bot.editMessageText(message['chat']['id'], message['message_id'], f'{msg}')

def accendiLuce(message):
    log(f"Accendo la luce per {message['message']['chat']['id']}")
    message = bot.sendAndGetMessage(message['message']['chat']['id'], "Provo ad accendere la luce")
    msg = ""
    try:
        resp = tuya.turnOn()
        if resp['header']['code'] == 'SUCCESS':
            msg = "Luce accesa"
        else:
            msg = "Errore nell'accensione della luce"
    except Exception as e:
        msg = f"Errore: {repr(e)}"
    log(f"Rispondo a {message['chat']['id'], message['message_id']} con {msg}")
    bot.editMessageText(message['chat']['id'], message['message_id'], f'{msg}')


def spegniLuce(message):
    log(f"Spengo la luce per {message['message']['chat']['id']}")
    message = bot.sendAndGetMessage(message['message']['chat']['id'], "Provo a spegnere la luce")
    msg = ""
    try:
        resp = tuya.turnOff()
        if resp['header']['code'] == 'SUCCESS':
            msg = "Luce spenta"
        else:
            msg = "Errore nello spegnimento della luce"
    except Exception as e:
        msg = f"Errore: {repr(e)}"
    log(f"Rispondo a {message['chat']['id'], message['message_id']} con {msg}")
    bot.editMessageText(message['chat']['id'], message['message_id'], f'{msg}')
    
def newToken(message):
    log(f"Richiedo un nuovo token per {message['message']['chat']['id']}")
    message = bot.sendAndGetMessage(message['message']['chat']['id'], "Richiedo un nuovo token")
    msg = ""
    try:
        tuya.getNewToken()
        access_token = tuya.getAccessToken()
        msg = f"Ho richiesto un nuovo token, {access_token}"
    except Exception as e:
        msg = f"Errore: {repr(e)}"
    log(f"Rispondo a {message['chat']['id'], message['message_id']} con {msg}")
    bot.editMessageText(message['chat']['id'], message['message_id'], f'{msg}')

def getLogFile(message):
    config = loadConfiguration()
    if f"{message['message']['chat']['id']}" == f'{config["chat_id_admin"]}':
        log(f"Invio il file di log a {message['message']['chat']['id']}")
        messageToEdit = bot.sendAndGetMessage(message['message']['chat']['id'], "Carico il file")
        bot.sendAction(message['message']['chat']['id'], utelegram.UPLOAD_DOCUMENT)
        f = open("logBot.txt", "r")
        #bot.sendFileAndGetMessage(message['message']['chat']['id'], f)
        lines = f.readlines()
        msg = "Ultime 5 righe del log\n===\n"
        msg += f"{lines[-5]}{lines[-4]}{lines[-3]}{lines[-2]}{lines[-1]}"
        f.close()
        bot.editMessageText(messageToEdit['chat']['id'], messageToEdit['message_id'], f'{msg}')
    else:
        log(f"{message['message']['chat']['id']} ha richiesto il file di log, ma NO")
        default_message_handler(message)



config = loadConfiguration()
bot = utelegram.ubot(config['bot_token'])

bot.register('/dispositivi', getDevices)
bot.register('/accendiluce', accendiLuce)
bot.register('/spegniluce', spegniLuce)
bot.register('/newtoken', newToken)
bot.register('/getLogFile', getLogFile)

bot.set_default_handler(default_message_handler)

def startBot():
    config = loadConfiguration()
    log("Ho avviato il bot")
    bot.send(f'{config["chat_id_admin"]}', 'Bot avviato')
    bot.listen()