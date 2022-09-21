import json

CONFIG_FILE = "config.json"

def loadConfiguration():
    f = open(CONFIG_FILE, "r")
    config = json.load(f)
    f.close()
    return config