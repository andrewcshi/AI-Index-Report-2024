import requests
from bs4 import BeautifulSoup

def get_authors(url):
    # Fetch the HTML content of the given URL
    response = requests.get(url)
    response.raise_for_status()  # This will raise an exception for HTTP errors

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div with class 'authors'
    authors_div = soup.find('div', class_='authors')

    # Initialize a list to store the authors' names
    authors_list = []

    # Check if the div was found
    if authors_div:
        # Find all anchor tags within the div
        anchor_tags = authors_div.find_all('a')

        # Extract the text from each anchor tag and add it to the list
        for tag in anchor_tags:
            authors_list.append(tag.get_text())

    return authors_list
