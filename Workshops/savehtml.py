import requests

url = 'https://icml.cc/virtual/2017/events/workshop'
response = requests.get(url)
with open('icmlworkshop17.html', 'w') as file:
    file.write(response.text)