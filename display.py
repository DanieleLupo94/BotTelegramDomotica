import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

#Init
disp.begin()


def scriviFrasi(frasi):
	if len(frasi) == 1:
		return scriviFraseMultiline(frasi[0])
	if len(frasi) > 8:
		print("Posso mostrare al massimo 8 frasi")

	disp.clear()
	disp.display()

	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))

	draw = ImageDraw.Draw(image)
	draw.rectangle((0,0,width,height), outline=0, fill=0)

	padding = -2
	top = padding
	bottom = height-padding
	x = 0

	font = ImageFont.load_default()

	draw.rectangle((0,0,width,height), outline=0, fill=0)

	y = top

	for frase in frasi:
		draw.text((x, y), frase, font=font, fill=255)
		y = y+8

	disp.image(image)
	disp.display()

def scriviFraseMultiline(frase):
	disp.clear()
	disp.display()

	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))

	draw = ImageDraw.Draw(image)
	draw.rectangle((0,0,width,height), outline=0, fill=0)

	padding = -2
	top = padding
	bottom = height-padding
	x = 0

	font = ImageFont.load_default()

	draw.rectangle((0,0,width,height), outline=0, fill=0)

	y = top

	for carattere in frase:
		draw.text((x, y), carattere, font=font, fill=255)
		x = x+6
		if x % 120 == 0:
			x = 0
			y = y+8

	disp.image(image)
	disp.display()

scriviFraseMultiline("Display avviato con successo")
#scriviFraseMultiline("Questa frase è davvero lunghissima quindi deve andare accapo")
