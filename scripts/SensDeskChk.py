# Version 0.001 - 20250902

import requests
from datetime import datetime
import xml.etree.ElementTree as ET
import sys

# Start EingabeParameter Checken
sendmsgdisc = False 
ListLogData = False

# Parameter msgon sendet Discord Nachrichten
# Parameter list gibt die Logfile Liste aus
# Funktion um die eingegebenen Parameter zu überprüfen und den Aufwand für Mehrfach Coding zu minimieren

def FunktionenCheckfunktion(AnzahlParameter):
    # global definiert Variablen aus dem Script innerhalb der Funktion
    global sendmsgdisc
    global ListLogData
    TextParameterGeht = "\nGültige Parameter sind\nmsgok - Sendet Nachrichten an Dicord\nlist - Gibt eine Detailierte Liste über alle Devices und Sensoren am Bildschirm aus\n"
    for loopzahl in range(1, int(AnzahlParameter)):
        if len(sys.argv) > loopzahl:
            paramxx = sys.argv[loopzahl]
            match paramxx:
                case "msgon":
                    sendmsgdisc = True 
                case "list":
                    ListLogData = True
                case "help":
                    print(TextParameterGeht)
                    sys.exit(0)
                case _:
                    print(paramxx + "ist kein gültiger Parameter\nDie Verarbeitung wurde Abgebrochen" + TextParameterGeht)
                    sys.exit(1)


FunktionenCheckfunktion(3)

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

# Globale Werte Zuweisen    
webhook_url = parameter_dict.get("webhook_url")
url = parameter_dict.get("url") 
MyLogFile = parameter_dict.get("MyLogFile")
writelog = parameter_dict.get("writelog")
# print(MyLogFile)
# r"C:\Users\MartinJestl\Downloads\python\jaylog.txt" # parameter_dict.get("MyLogFile")
jetzt = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
LogFileText = "Neuer Eintrag - " + jetzt + "\n"
AlarmGefunden = False
DiscordText = "Zusammenfassung vom " + jetzt + "\n"
DiscordSend = False
# XML Analyse

print("Lade und analysiere die Daten")

# XML-Daten vom Server laden
response = requests.get(url)
if response.status_code == 200:
    # XML-Inhalt parsen
    root = ET.fromstring(response.content)
    
    # Beispiel: Alle Tag-Namen und deren Text ausgeben
    # for child in root:
    #   print(child.tag, child.text)


    # Werte aus Root -> Agent auslesen
    agent = root.find('Agent')
    version = agent.find('Ver').text
    name = agent.find('Name').text
    timestamp = agent.find('Timestamp').text

    LogFileText += f"Agent Version: {version}\n"
    LogFileText += f"Agent Name: {name}\n"
    LogFileText += f"Agent Timestamp: {timestamp}\n"

    # Iterate über alle Devices
    for device in root.find('Devices').findall('Device'):
        dev_id = device.get('dev_id')
        device_agent = device.find('Agent')
        device_name = device_agent.find('Alias').text
        mac = device_agent.find('MAC').text
        model = device_agent.find('Model').text
        model_devtype_id = device_agent.find('Model').get('devtype_id')
        status = device_agent.find('Status').text

        LogFileText += f"\n... Gerät ...\n"
        LogFileText += f"\nDevice ID: {dev_id}\n"
        LogFileText += f"Device Name: {device_name}\n"
        LogFileText += f"Model: {model} (devtype_id={model_devtype_id})\n"
        LogFileText += f"Status: {status}\n"
        LogFileText += f"\n-- Sensoren --\n"

        # mit .//Sensors suche ich in beliebiger Teife den Wert Senors vom Array device
        for lsensor in device.find('.//Sensors').findall('Sensor'):
            lsens_id = lsensor.get('sens_id')
            lname = lsensor.find('Alias').text 
            lsvalue = float(lsensor.find('Value').text)/10
            lunits = lsensor.find('Units').text
            ls_zeit = lsensor.find('Timestamp').text
            lsensoralarm = lsensor.find('Status/Alarm').text

            LogFileText += f"    --------\n"
            LogFileText += f"    Device: {device_name}\n"
            LogFileText += f"    Sensor ID: {lsens_id}\n"
            LogFileText += f"    Sensor Name: {lname}\n"
            LogFileText += f"    Sensor Value: {lsvalue} {lunits}\n"
            LogFileText += f"    Sensor Alarm: {lsensoralarm}\n\n"
            if int(lsensoralarm) == 1: 
                #and sendmsgdisc == True:
                AlarmGefunden = True
                DiscordText += f"    --------\n"
                DiscordText += f"    Device: {device_name}\n"
                DiscordText += f"    Sensor ID: {lsens_id}\n"
                DiscordText += f"    Sensor Name: {lname}\n"
                DiscordText += f"    Sensor Value: {lsvalue} {lunits}\n"
                DiscordText += f"    Sensor Alarm: {lsensoralarm}\n\n"
                DiscordSend = True

    
    print("Daten erfolgreich Geladen und verarbeitet")
else:
    
    print(f"Fehler beim Laden der Daten: {response.status_code}")


if AlarmGefunden == True:
    print("Alarm Gefunden!!")
    LogFileText += f"\n### Errors ### \n\n" + DiscordText
else:
    print("Alles Bestens")
    LogFileText += f"\n ### Alles OK ### \n"

LogFileText += f"\n\nLog Ende\n###################################################\n"

if writelog == "j" or writelog == "y":    
    # Logfile Schreiben   
    with open(MyLogFile, "a") as datei:
            datei.write(LogFileText)

# Discord Webhook Sender
if DiscordSend == True and sendmsgdisc == True:   
            #Send Errormsg
            if AlarmGefunden == False:
                DiscordText += "Keine Fehler Gefunden"

            data = {
                'content': DiscordText,
                'username': 'MartinsSensDeskBot'  # Optional: Absendername
                }

            response = requests.post(webhook_url, json=data)

            if response.status_code == 204:
                print('Discord Nachricht erfolgreich gesendet!')
            else:
                print(f'Fehler: {response.status_code}')    
if ListLogData == True:
    print("\n\n ######## Daten Ausgabe ######## \n\n")
    print(LogFileText)

# Ende der Verarbeitung