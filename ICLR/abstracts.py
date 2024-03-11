import requests
from bs4 import BeautifulSoup
import time

def get_abstracts(url):
    # Send a GET request to fetch the page content
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div tag with the specified id
    div_tag = soup.find('div', id='abstractExample')

    # Initialize an empty string for the paragraph text
    paragraph_text = ''

    # Check if the div tag was found
    if div_tag:
        # Find the first p tag within the div tag
        p_tag = div_tag.find('p')
        
        # Check if the p tag was found
        if p_tag:
            # Extract the text from the p tag
            paragraph_text = p_tag.text
            paragraph_text = paragraph_text.strip()
            paragraph_text = paragraph_text.replace('\n','')

    return paragraph_text

### TESTING ###
# url = 'https://iclr.cc/virtual/2020/poster/2057'
# print(get_abstracts(url))