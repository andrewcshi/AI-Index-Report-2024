import requests

url = 'https://iclr.cc/virtual/2020/papers.html?filter=titles'
response = requests.get(url)
with open('iclrpapers20.html', 'w') as file:
    file.write(response.text)