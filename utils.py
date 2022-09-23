import json

CONFIG_FILE = "config.json"

def loadConfiguration():
    f = open(CONFIG_FILE, "r")
    config = json.load(f)
    f.close()
    return config

def saveConfiguration(config):
    f = open(CONFIG_FILE, "w+")
    json.dump(config, f)
    f.close()
    return True