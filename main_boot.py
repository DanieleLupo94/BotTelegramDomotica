import json
import utelegram
import json

CONFIG_FILE = "config.json"

def loadConfiguration():
    return json.load(open(CONFIG_FILE, "a+"))

def default_message_handler(message):
    bot.send(message['message']['chat']['id'], 'Ti ho letto')

config = loadConfiguration()
bot = utelegram.ubot(config['bot_token'])
bot.set_default_handler(default_message_handler)
bot.listen()