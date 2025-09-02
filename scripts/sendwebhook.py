import requests

webhook_url = 'https://discord.com/api/webhooks/1412321293222674515/Ee6fjp9_Zp5p7tzi9Y1MNfn_myN-qo4E6VTdxWsnjWdGAgAkjU4R5yI1b6YCxdZ_cpwi'
data = {
    'content': 'Hallo, Discord!',
    'username': 'MartinsSensDeskBot'  # Optional: Absendername
    # Optional: 
    'avatar_url': 'https://gravatar.com/avatar/bbfbc285d1d9eefdfa2afa876374b687a90f13e6ab345bdee46fc19230152441?v=1756788547000&size=256&d=initials'
}

response = requests.post(webhook_url, json=data)

if response.status_code == 204:
    print('Nachricht erfolgreich gesendet!')
else:
    print(f'Fehler: {response.status_code}')
