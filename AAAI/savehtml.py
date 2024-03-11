import requests

url = 'https://dblp.org/db/conf/aaai/aaai2023.html'
response = requests.get(url)
with open('aaai23.html', 'w') as file:
    file.write(response.text)