import requests
from bs4 import BeautifulSoup

def get_authors(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the h3 tag with the specified class
        h3_tag = soup.find('h3', class_='card-subtitle mb-2 text-muted text-center')
        if h3_tag:
            # Access the text within the h3 tag, strip extra spaces, and split by '·' to get individual names
            authors = [author.strip() for author in h3_tag.text.split('·')]
            return authors
        else:
            # Return an empty list if the tag is not found
            return []
    else:
        # Return an empty list if the request was unsuccessful
        return []

### TESTING ###
# url = 'https://iclr.cc/virtual/2020/poster/2057'
# print(get_authors(url))