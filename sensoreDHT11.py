import Adafruit_DHT
import time

sensore = Adafruit_DHT.DHT11
pin = 4

def readHumidityTemperature():
	h0, t0 = Adafruit_DHT.read_retry(sensore, pin)
	#print('Temperatura={0:0.1f}C Humidity={1:0.1f}%'.format(t0, h0))
	time.sleep(2)
	h1, t1 = Adafruit_DHT.read_retry(sensore, pin)
	#print('Temperatura={0:0.1f}C Humidity={1:0.1f}%'.format(t1, h1))
	time.sleep(2)
	h2, t2 = Adafruit_DHT.read_retry(sensore, pin)
	#print('Temperatura={0:0.1f}C Humidity={1:0.1f}%'.format(t2, h2))
	h = min(h0, h1, h2)
	t = min(t0, t1, t2)
	return h, t
