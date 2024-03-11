import requests
from bs4 import BeautifulSoup
import time

def get_abstracts(url):
    try:
        page_response = requests.get(url)

        if page_response.status_code == 200:
            page_soup = BeautifulSoup(page_response.content, 'html.parser')
            abstract_tag = page_soup.find('blockquote', class_='abstract mathjax')
            
            if abstract_tag:
                return abstract_tag.get_text().strip()[9:]
            else:
                print(f"No abstract found for {url}")
        else:
            print(f"Failed to fetch {url}, status code: {page_response.status_code}")
        
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        
    return None

### TESTING ###
# url = 'https://arxiv.org/abs/2307.11806'
# result = get_abstracts(url)
# print(result)