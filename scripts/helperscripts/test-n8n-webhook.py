import requests

webhook_url = 'http://192.168.200.225:5678/webhook-test/f37baba5-7d1a-4cf1-bce9-0fd35de109c8'
data = {
    'content': 'Hallo, Discord!',
    'username': 'MartinsSensDeskBot'  # Optional: Absendername
    # Optional: 
    #'avatar_url': 'https://media-cdn.ubuntu-de.org/wiki/thumbnails/2/25/2547aa926ad69a2e4547a290ba7c9874e6405ea6i64x.png'
}

# Parameter, die du per GET senden willst
params = {
    "Vorname": "martin",
    "Sender": "Windows11"
}

# GET-Anfrage mit Parametern
response = requests.get(webhook_url, params=params)

print(f"Statuscode: {response.status_code}")
print(f"Antwort: {response.text}")