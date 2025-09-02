print("Load Data")

from datetime import datetime
import requests
import xml.etree.ElementTree as ET

# URL des XML-Webservers
url = 'https://sensdesk.at/sensdesk/user/898/values.xml?values_xml_key=dfbkSLU74ZhtPg_7wG8YktPN-xpfEs8VMF-mYJwpaO8'

# XML-Daten vom Server laden
response = requests.get(url)
if response.status_code == 200:
    # XML-Inhalt parsen
    root = ET.fromstring(response.content)
    
    # Beispiel: Alle Tag-Namen und deren Text ausgeben
    for child in root:
        print(child.tag, child.text)


    # Werte aus Root -> Agent auslesen
agent = root.find('Agent')
version = agent.find('Ver').text
name = agent.find('Name').text
timestamp = agent.find('Timestamp').text

print(f"Agent Version: {version}")
print(f"Agent Name: {name}")
print(f"Agent Timestamp: {timestamp}")

# Iterate über alle Devices
for device in root.find('Devices').findall('Device'):
    dev_id = device.get('dev_id')
    device_agent = device.find('Agent')
    device_name = device_agent.find('Name').text
    mac = device_agent.find('MAC').text
    model = device_agent.find('Model').text
    model_devtype_id = device_agent.find('Model').get('devtype_id')
    status = device_agent.find('Status').text

    print(f"\nDevice ID: {dev_id}")
    print(f"Device Name: {device_name}")
    print(f"MAC-Adresse: {mac}")
    print(f"Model: {model} (devtype_id={model_devtype_id})")
    print(f"Status: {status}")

    time = device.find('Time')
    timezone = time.find('Timezone').text
    dst = time.find('Dst').text
    time_stamp = time.find('Timestamp').text

    print("Time info:")
    print(f"  Timezone: {timezone}")
    print(f"  DST: {dst}")
    print(f"  Timestamp: {time_stamp}")

# Sensoren Laden

# Alle Sensoren finden
sensors = root.findall('.//Sensor')

for sensor in sensors:
    sens_id = sensor.get('sens_id')
    name = sensor.find('Name').text 
    id = sensor.find('ID').text
    svalue = float(sensor.find('Value').text)/10
    units = sensor.find('Units').text
    zeit = sensor.find('Timestamp').text
    sensoralarm = sensor.find('Status/Alarm').text

    print(f"\nSensor ID: {sens_id}")
    print(f"Sensor Name: {name}")
    print(f"Sensor Value: {svalue} {units}")
    print(f"Sensor Timestamp: {zeit}")
    print(f"Sensor Alarm: {sensoralarm}")

else:
    print(f"Fehler beim Laden der Daten: {response.status_code}")

