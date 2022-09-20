import utelegram
import json
import tuya_micropython as tuya

CONFIG_FILE = "config.json"

def loadConfiguration():
    return json.load(open(CONFIG_FILE, "a+"))

def default_message_handler(message):
    bot.send(message['message']['chat']['id'], f"Ti ho letto {message}")

def getDevices(message):
    message = bot.sendAndGetMessage(message['message']['chat']['id'], "Recupero i dispositivi")
    msg = ""
    try:
        d = tuya.getDevices()
        msg = f"{d}"
    except Exception as e:
        msg = f"Errore: {e}"
    bot.editMessageText(message['chat']['id'], message['message_id'], f'{msg}')

def accendiLuce(message):
    message = bot.sendAndGetMessage(message['message']['chat']['id'], "Provo ad accendere la luce")
    msg = ""
    try:
        resp = tuya.turnOn()
        if resp['header']['code'] == 'SUCCESS':
            msg = "Luce accesa"
        else:
            msg = "Errore nell'accensione della luce"
    except Exception as e:
        msg = f"Errore: {e}"
    bot.editMessageText(message['chat']['id'], message['message_id'], f'{msg}')


def spegniLuce(message):
    message = bot.sendAndGetMessage(message['message']['chat']['id'], "Provo a spegnere la luce")
    msg = ""
    try:
        resp = tuya.turnOff()
        if resp['header']['code'] == 'SUCCESS':
            msg = "Luce spenta"
        else:
            msg = "Errore nello spegnimento della luce"
    except Exception as e:
        msg = f"Errore: {e}"
    bot.editMessageText(message['chat']['id'], message['message_id'], f'{msg}')
    
def newToken(message):
    message = bot.sendAndGetMessage(message['message']['chat']['id'], "Richiedo un nuovo token")
    msg = ""
    try:
        tuya.getNewToken()
        access_token = tuya.getAccessToken()
        msg = f"Ho richiesto un nuovo token, {access_token}"
    except Exception as e:
        msg = f"Errore: {e}"
    bot.editMessageText(message['chat']['id'], message['message_id'], f'{msg}')


config = loadConfiguration()
bot = utelegram.ubot(config['bot_token'])

bot.register('/dispositivi', getDevices)
bot.register('/accendiluce', accendiLuce)
bot.register('/spegniluce', spegniLuce)
bot.register('/newtoken', newToken)

bot.set_default_handler(default_message_handler)

def startBot():
    config = loadConfiguration()
    bot.send(config["chat_id_admin"], 'Bot avviato')
    bot.listen()