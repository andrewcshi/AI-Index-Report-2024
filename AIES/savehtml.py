import requests

url = 'https://www.aies-conference.com/2018/accepted-papers/'
response = requests.get(url)
with open('aies18.html', 'w') as file:
    file.write(response.text)