import requests

url = 'https://nips.cc/virtual/2022/papers.html?filter=titles'
response = requests.get(url)
with open('neurips22keywords.html', 'w') as file:
    file.write(response.text)