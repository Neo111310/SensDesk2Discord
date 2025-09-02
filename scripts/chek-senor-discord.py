# Version 0.001 - 20250902

import requests
from datetime import datetime
import xml.etree.ElementTree as ET
import sys

# Start Parameter Checken
sendmsgdisc = False 

if len(sys.argv) > 1:
    param1 = sys.argv[1]
    if param1 == "msgon":
        sendmsgdisc = True 


# Globale Parameter aus der Config datei Laden
# Webhook vom Discord-Server
# webhook_url = 'https://discord.com/api/webhooks/1412321293222674515/Ee6fjp9_Zp5p7tzi9Y1MNfn_myN-qo4E6VTdxWsnjWdGAgAkjU4R5yI1b6YCxdZ_cpwi'
# URL des XML-Webservers
# url = 'https://sensdesk.at/sensdesk/user/898/values.xml?values_xml_key=dfbkSLU74ZhtPg_7wG8YktPN-xpfEs8VMF-mYJwpaO8'

# Lesen der Konfigurationsdatei
import os
parameter_dict = {}

script_dir = os.path.dirname(os.path.abspath(__file__))
dateipfad = os.path.join(script_dir, "jay.config")

with open(dateipfad, "r") as file:
    for line in file:
        line = line.strip()
        # Kommentarzeilen überspringen
        if line.startswith("#") or not line:
            continue
        # String an Doppelpunkt splitten
        if ":" in line:
            param, wert = line.split(":", 1)
            param = param.strip()
            wert = wert.strip()
            # Wert zu Parameter im Dictionary speichern
            parameter_dict[param] = wert

# Werte Zuweisen    
webhook_url = parameter_dict.get("webhook_url")
url = parameter_dict.get("url") 
MyLogFile = parameter_dict.get("MyLogFile")
writelog = parameter_dict.get("writelog")
# r"C:\Users\MartinJestl\Downloads\python\jaylog.txt" # parameter_dict.get("MyLogFile")
jetzt = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
LogFileText = "Neuer Eintrag - " + jetzt + "\n"
# XML Analyse

# XML-Daten vom Server laden
response = requests.get(url)
if response.status_code == 200:
    # XML-Inhalt parsen
    root = ET.fromstring(response.content)
    
    # Beispiel: Alle Tag-Namen und deren Text ausgeben
    # for child in root:
    #     print(child.tag, child.text)


    # Werte aus Root -> Agent auslesen
    agent = root.find('Agent')
    version = agent.find('Ver').text
    name = agent.find('Name').text
    timestamp = agent.find('Timestamp').text

    print(f"Agent Version: {version}")
    LogFileText += f"Agent Version: {version}\n"
    print(f"Agent Name: {name}")
    LogFileText += f"Agent Name: {name}\n"
    print(f"Agent Timestamp: {timestamp}")
    LogFileText += f"Agent Timestamp: {timestamp}\n"

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
        LogFileText += f"\nDevice ID: {dev_id}\n"
        print(f"Device Name: {device_name}")
        LogFileText += f"Device Name: {device_name}\n"
        print(f"MAC-Adresse: {mac}")
        LogFileText += f"MAC-Adresse: {mac}\n"
        print(f"Model: {model} (devtype_id={model_devtype_id})")
        LogFileText += f"Model: {model} (devtype_id={model_devtype_id})\n"
        print(f"Status: {status}")
        LogFileText += f"Status: {status}\n"

        time = device.find('Time')
        timezone = time.find('Timezone').text
        dst = time.find('Dst').text
        time_stamp = time.find('Timestamp').text
        DatumZeitSensDesk = datetime.fromtimestamp(int(time_stamp)).strftime('%d.%m.%Y %H:%M:%S')

        print("Time info:")
        LogFileText += "Time info:\n"
        print(f"  Timezone: {timezone}")
        LogFileText += f"  Timezone: {timezone}\n"
        print(f"  DST: {dst}")
        LogFileText += f"  DST: {dst}\n"
        print(f"  Timestamp: {DatumZeitSensDesk}")
        LogFileText += f"  Timestamp: {DatumZeitSensDesk}\n"

    # Sensoren Laden

    # Alle Sensoren finden
    sensors = root.findall('.//Sensor')

    for sensor in sensors:
        sens_id = sensor.get('sens_id')
        name = sensor.find('Name').text 
        id = sensor.find('ID').text
        svalue = float(sensor.find('Value').text)/10
        units = sensor.find('Units').text
        s_zeit = sensor.find('Timestamp').text
        sensoralarm = sensor.find('Status/Alarm').text
        zeit = datetime.fromtimestamp(int(s_zeit)).strftime('%d.%m.%Y %H:%M:%S')

        print(f"\nSensor ID: {sens_id}")
        LogFileText += f"\nSensor ID: {sens_id}\n"
        print(f"Sensor Name: {name}")
        LogFileText += f"Sensor Name: {name}\n"
        print(f"Sensor Value: {svalue} {units}")
        LogFileText += f"Sensor Value: {svalue} {units}\n"
        print(f"Sensor Timestamp: {zeit}")
        LogFileText += f"Sensor Timestamp: {zeit}\n"
        print(f"Sensor Alarm: {sensoralarm}")
        LogFileText += f"Sensor Alarm: {sensoralarm}\n"
        print(f"Zeitpunkt {zeit}")
        LogFileText += f"Zeitpunkt {zeit}\n"

        if int(sensoralarm) == 1 and sendmsgdisc == True:   
            #Send Errormsg
            data = {
                'content': f'Hallo Martin, Fehlermeldung -- ID:{sens_id} - Name: {name} - Wert: {svalue} {units} - Zeit: {zeit} - Alarm: {sensoralarm}',
                'username': 'MartinsSensDeskBot'  # Optional: Absendername
                }

            response = requests.post(webhook_url, json=data)

            if response.status_code == 204:
                print('Discord Nachricht erfolgreich gesendet!')
            else:
                print(f'Fehler: {response.status_code}')
    print("Daten erfolgreich Geladen und verarbeitet")
else:
    
    print(f"Fehler beim Laden der Daten: {response.status_code}")


LogFileText += f"Log Ende\n###################################################\n"

if writelog == "j":    
    # Logfile Schreiben   
    with open(MyLogFile, "a") as datei:
            datei.write(LogFileText)

# Ende der Verarbeitung