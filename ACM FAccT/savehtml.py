import requests

url = 'https://facctconference.org/2019/acceptedpapers'
response = requests.get(url)
with open('facctpapers19.html', 'w') as file:
    file.write(response.text)