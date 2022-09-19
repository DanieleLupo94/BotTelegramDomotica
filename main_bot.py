import json
import utelegram
import json
import tuya_micropython as tuya

CONFIG_FILE = "config.json"

def loadConfiguration():
    return json.load(open(CONFIG_FILE, "a+"))

def default_message_handler(message):
    bot.send(message['message']['chat']['id'], 'Ti ho letto')

def getDevices(message):
    print(f'Recupero i dispositivi')
    d = tuya.getDevices()
    bot.send(message['message']['chat']['id'], f'{d}')

def accendiLuce(message):
    bot.sendAction(message['message']['chat']['id'], f'{utelegram.TYPING}')
    resp = tuya.turnOn()
    msg = ""
    if resp['header']['code'] == 'SUCCESS':
        msg = "Luce accesa"
    else:
        msg = "Errore nell'accensione della luce"
    bot.send(message['message']['chat']['id'], f'{msg}')

def spegniLuce(message):
    bot.sendAction(message['message']['chat']['id'], f'{utelegram.TYPING}')
    resp = tuya.turnOff()
    msg = ""
    if resp['header']['code'] == 'SUCCESS':
        msg = "Luce spenta"
    else:
        msg = "Errore nello spegnimento della luce"
    bot.send(message['message']['chat']['id'], f'{msg}')

def newToken(message):
    tuya.getNewToken()
    bot.send(message['message']['chat']['id'], "Ho richiesto un nuovo token")


config = loadConfiguration()
bot = utelegram.ubot(config['bot_token'])

bot.register('/dispositivi', getDevices)
bot.register('/accendiluce', accendiLuce)
bot.register('/spegniluce', spegniLuce)
bot.register('/newtoken', newToken)

bot.set_default_handler(default_message_handler)

bot.listen()