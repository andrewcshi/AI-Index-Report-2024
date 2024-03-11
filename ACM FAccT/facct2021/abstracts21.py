import requests
from bs4 import BeautifulSoup
import time

def get_abstracts(url):
    """
    Retrieves the abstract from an academic paper's webpage given its URL.
    This function sends a request to the url and parses the HTML content to extract the abstract of the paper.

    Parameters:
    url (str): The URL of the paper's webpage from which to extract the abstract.

    Returns:
    abstract: The text of the abstract. Returns None if the abstract is not found, the request fails, or an exception occurs.
    """
    
    try:
        # Send a GET request to each URL
        page_response = requests.get(url)

        # Check if the request was successful
        if page_response.status_code == 200:
            page_soup = BeautifulSoup(page_response.content, 'html.parser')
            abstract_tag = page_soup.find('div', class_='abstractSection')
            
            # Extract and add the text of the abstract if it exists
            if abstract_tag:
                return abstract_tag.get_text().strip()
            else:
                print(f"No abstract found for {url}")
        else:
            print(f"Failed to fetch {url}, status code: {page_response.status_code}")
        
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        
    return None

### TESTING ###
# url = 'https://doi.org/10.1145/3593013.3594084'
# result = get_abstracts(url)
# print(result)