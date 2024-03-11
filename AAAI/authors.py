import requests
from bs4 import BeautifulSoup

def get_authors(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    authors_div = soup.find('div', class_='authors')

    authors_list = []

    if authors_div:
        anchor_tags = authors_div.find_all('a')

        for tag in anchor_tags:
            authors_list.append(tag.get_text())

    return authors_list

### TESTING ###
# url = 'https://arxiv.org/abs/2206.07635'
# print(get_authors(url))