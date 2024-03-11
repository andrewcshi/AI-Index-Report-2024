import requests
from bs4 import BeautifulSoup
import time

def get_abstracts(url):
    try:
        # Send a GET request to each URL
        page_response = requests.get(url)

        # Check if the request was successful
        if page_response.status_code == 200:
            page_soup = BeautifulSoup(page_response.content, 'html.parser')
            abstract_tag = page_soup.find('blockquote', class_='abstract mathjax')
            
            # Extract and add the text of the abstract if it exists
            if abstract_tag:
                abstract_tag = abstract_tag.get_text().strip()[9:]
                abstract_tag = abstract_tag.replace('\n', '')
                return abstract_tag
            else:
                print(f"No abstract found for {url}")
        else:
            print(f"Failed to fetch {url}, status code: {page_response.status_code}")
        
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        
    return None

### TESTING ###
# url = 'https://arxiv.org/abs/2205.10423'
# print(get_abstracts(url))