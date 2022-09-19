import urequests as requests
import json

# TODO: Rendere tutto generico e chiamabile dal main_boot

CONFIG_FILE = "tuyaConfig.json"

def loadConfiguration():
    return json.load(open(CONFIG_FILE, "r"))

def readAccessTokenFromFile():
	try:
		return json.load(open("access_token", "r+"))
	except:
		return None
		
def getAccessToken():
	fromFile = readAccessTokenFromFile()
	if fromFile is not None:
		print(f"Ho letto il token dal file {fromFile}")
		access_token = fromFile["access_token"]
		return access_token

	print("Richiedo il token")
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
	print(f'{auth}')
	try:
		auth["responseStatus"]
		if auth["responseStatus"] == 'error':
			return None
	except KeyError as e:
		pass
	access_token = auth["access_token"]
	#refresh_token = auth["refresh_token"]
	print("Scrivo il token sul file")
	print(f"{{\"access_token\":\"{access_token}\"}}", file=open("access_token", "w+"))
	return access_token

def getDevices():
	access_token = getAccessToken()
	print(f'access_token {access_token}')
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
	print("Reset token")
	f = open("access_token", "w")
	f.close()
	getAccessToken()
