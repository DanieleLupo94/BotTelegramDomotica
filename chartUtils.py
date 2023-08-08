import matplotlib.pyplot as plt
import datetime


def createChart():
    daily_data = {}

    with (open("/home/pi/temperature.csv", "r")) as f:
        allLines = f.readlines()
        allLines.reverse()
        for l in allLines:
            l = l.strip()
            l = l.replace("\x00", "")
            if len(l) < 1:
                continue
            values = l.split(",")
            temperature = float(values[0])
            humidity_value = float(values[2])
            timestamp_ms = int(values[1])

            timestamp_sec = timestamp_ms / 1000.0
            date_object = datetime.fromtimestamp(timestamp_sec)
            date_only = date_object.date()

            if date_only in daily_data:
                # If the date already exists, update the daily values
                daily_data[date_only]['temperature'].append(temperature)
                daily_data[date_only]['humidity'].append(humidity_value)
            else:
                # If the date doesn't exist, create a new entry
                daily_data[date_only] = {
                    'temperature': [temperature],
                    'humidity': [humidity_value]
                }

    daily_averages = {}
    xValues = []
    yTemp = []
    yHum = []
    for date, data in daily_data.items():
        avg_temperature = sum(data['temperature']) / len(data['temperature'])
        avg_humidity = sum(data['humidity']) / len(data['humidity'])
        daily_averages[date] = {
            'average_temperature': avg_temperature,
            'average_humidity': avg_humidity
        }
        xValues.append(date)
        yTemp.append(int(avg_temperature))
        yHum.append(int(avg_humidity))
    maxTemp = max(yTemp)
    maxTemp = int(maxTemp)
    maxHum = max(yHum)
    maxHum = int(maxHum)

    minTemp = min(yTemp)
    minTemp = int(minTemp)
    minHum = min(yHum)
    minHum = int(minHum)

    plt.figure(figsize=(20, 12))  # Set the figure size (adjust as needed)

    plt.plot(xValues, yTemp, label='Temperature')
    plt.plot(xValues, yHum, label='Humidity')

    textPosition = len(xValues)/2 + len(xValues)/4
    # print(f'{textPosition}')

    textPosition = xValues[int(textPosition)]

    plt.axhline(maxTemp, color='red', linestyle='--',
                label=f'Max temperature {maxTemp}')

    plt.text(textPosition, maxTemp, f'Max temperature = {maxTemp}°C', color='red',
             fontsize=10, ha='right', va='bottom')

    plt.axhline(minTemp, color='darkorange', linestyle='--',
                label=f'Min temperature {minTemp}')

    plt.text(textPosition, minTemp, f'Min temperature = {minTemp}°C', color='darkorange',
             fontsize=10, ha='right', va='bottom')

    plt.axhline(maxHum, color='blue', linestyle='--',
                label=f'Max humidity {maxHum}')

    plt.text(textPosition, maxHum, f'Max humidity = {maxHum}%', color='blue',
             fontsize=10, ha='right', va='bottom')

    plt.axhline(minHum, color='deepskyblue', linestyle='--',
                label=f'Min humidity {minHum}')

    plt.text(textPosition, minHum, f'Min humidity = {minHum}%', color='deepskyblue',
             fontsize=10, ha='right', va='bottom')

    plt.xlabel('Time')
    plt.ylabel('Temperature and Humidity')
    plt.title('Temperature and Humidity over time')
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plt.close()

    return buf
