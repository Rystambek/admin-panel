import requests
import os

url = 'https://instadownloderbot.pythonanywhere.com/webhook'

Token = '5696117143:AAH3Ej-BE4VgykO6NlKHUxYDQISbN85CzR0'

payload = {
    "url":url
}

r = requests.get(f"https://api.telegram.org/bot{Token}/setWebhook", params=payload)
r = requests.get(f"https://api.telegram.org/bot{Token}/GetWebhookInfo", params=payload)



print(r.json())