import csv
import datetime

def readFromFile(file = "/home/pi/temperature.csv"):
	allValues = []
	with open(file, "r", newline="\n") as f:
		spamreader = csv.reader((line.replace('\0','') for line in f), delimiter=',', quotechar='|')
		for row in spamreader:
			if len(row) < 3:
				continue
			allValues.append({"temperature": f"{row[0]}", "timestamp": int(row[1]), "humidity":f"{row[2]}"})
	return allValues
	
def readLastValue(file = "/home/pi/temperature.csv"):
	allValues = readFromFile()
	if len(allValues) > 0:
		return allValues[-1]
	return None

lastValue = readLastValue()
print(f'Vorrei convertire {int(lastValue["timestamp"])/1000.0}')
when = datetime.datetime.fromtimestamp(int(lastValue["timestamp"])/1000.0)
when = when.strftime('%d/%m/%Y %H:%M:%S')
print(f'[{when}] {lastValue["temperature"]}° e {lastValue["humidity"]}% umidità')
