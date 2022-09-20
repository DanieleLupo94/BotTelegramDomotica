import urequests as requests
import json

# TODO: Rendere tutto generico e chiamabile dal main_boot

CONFIG_FILE = "tuyaConfig.json"

def loadConfiguration():
    return json.load(open(CONFIG_FILE, "r"))

def writeAccessToken(access_token):
	t = {"access_token":access_token}
	f = open("access_token", "w")
	json.dump(t, f)
	f.close()

def readAccessTokenFromFile():
	try:
		r = json.load(open("access_token", "r"))
		return r
	except:
		return None
		
def getAccessToken():
	fromFile = readAccessTokenFromFile()
	if fromFile is not None and fromFile['access_token'] != '':
		access_token = fromFile["access_token"]
		return access_token

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
	return turnon
	
def turnOff():
	config = loadConfiguration()
	access_token = getAccessToken()
	turnoff = requests.post(
	"https://px1.tuyaus.com/homeassistant/skill",
	json={"header": {"name": "turnOnOff", "namespace": "control", "payloadVersion": 1}, "payload": {"accessToken": access_token, "devId": f'{config["idLuce"]}', "value":"0"}}).json()
	return turnoff

def refreshToken():
	global access_token
	global refresh_token
	if (access_token == '' or refresh_token == ''):
		return getAccessToken()
	auth = requests.post(
		"https://px1.tuyaus.com/homeassistant/access.do",
		data={
			"grant_type": "refresh_token",
			"refresh_token": refresh_token,
			"rand": 23
		},
	).json()
	access_token = auth["access_token"]
	refresh_token = auth["refresh_token"]

def getNewToken():
	writeAccessToken("")
	getAccessToken()
