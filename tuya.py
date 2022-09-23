import requests
import json
from utils import loadConfiguration
from utils import saveConfiguration

# TODO: Rendere tutto generico e chiamabile dal main_boot

CONFIG_FILE = "config.json"

def writeAccessToken(access_token):
	config = loadConfiguration()
	config["access_token"] = access_token
	saveConfiguration(config)

def readAccessTokenFromFile():
	try:
		config = loadConfiguration()
		return config["access_token"]
	except:
		return None
		
def getAccessToken():
	fromFile = readAccessTokenFromFile()
	if fromFile is not None and fromFile != '':
		return fromFile

	config = loadConfiguration()
	data={
			"userName": f"{config['username']}",
			"password": f"{config['password']}",
			"countryCode": f"{config['countryCode']}",
			"bizType": f"{config['bizType']}",
			"from": f"{config['from']}"
		}
	data_encoded = ""
	for k in data.keys():
		data_encoded = f'{data_encoded}&{k}={data[k]}'
	auth = requests.post("https://px1.tuyaus.com/homeassistant/auth.do", headers={"Content-Type": "application/x-www-form-urlencoded"}, data=data_encoded).json()
	if auth['access_token'] is None:
		raise Exception(f'{auth}')
	access_token = auth["access_token"]
	writeAccessToken(access_token)
	#refresh_token = auth["refresh_token"]
	return access_token

def getDevices():
	access_token = getAccessToken()
	devices = requests.post(
    "https://px1.tuyaus.com/homeassistant/skill",
    json={"header": {"name": "Discovery", "namespace": "discovery", "payloadVersion": 1}, "payload": {"accessToken": access_token}}).json()
	return devices

def turnOn():
	config = loadConfiguration()
	access_token = getAccessToken()
	turnon = requests.post(
    "https://px1.tuyaus.com/homeassistant/skill",
    json={"header": {"name": "turnOnOff", "namespace": "control", "payloadVersion": 1}, "payload": {"accessToken": access_token, "devId": f'{config["idLuce"]}', "value":"1"}}).json()
	if turnon['header']['code'] in 'SUCCESS':
		return True
	else:
		return False
	
def turnOff():
	config = loadConfiguration()
	access_token = getAccessToken()
	turnoff = requests.post(
	"https://px1.tuyaus.com/homeassistant/skill",
	json={"header": {"name": "turnOnOff", "namespace": "control", "payloadVersion": 1}, "payload": {"accessToken": access_token, "devId": f'{config["idLuce"]}', "value":"0"}}).json()
	if turnoff['header']['code'] in 'SUCCESS':
		return True
	else:
		return False

def getNewToken():
	writeAccessToken("")
	return True, getAccessToken()
