import requests
from bs4 import BeautifulSoup

def get_keywords(url):
    """
    Extracts keywords from an academic paper's url.
    This function first parses the initial HTML response to extract the reference number. It then
    constructs a new url to access the HTML content of the paper and extracts keywords form that webpage.

    Parameters:
    response (requests.Response): The initial response object from a GET request to the paper's page.
    url (str): The URL from which the response was obtained. Used to construct the full link to the paper.

    Returns:
    list of str: A list of extracted keywords from the paper's webpage. Returns None if the request fails or if an exception occurs.
    """
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <a> tags with the specified class
    tags = soup.find_all('a', class_='text-secondary text-decoration-none')
    
    # Extract and store the text from each tag
    keywords = [tag.get_text() for tag in tags]
    
    return keywords

### TESTING ###
# url = 'https://nips.cc/virtual/2022/poster/53809'
# result = get_keywords(url)
# print(result)