import requests
from bs4 import BeautifulSoup
import time

def get_authors(response, url):
    """
    Extracts authors and their affiliations from an academic paper's url.
    This function sends a request to the provided URL to fetch the full HTML content of the paper. 
    It then parses the response to extract the names of authors and their affiliations.

    Parameters:
    response (requests.Response): The initial response object from a request to the paper's page.
    url (str): The URL from which the response was obtained. Used to send a new request to fetch the full content.

    Returns:
    paper_authors_affiliations: A dictionary where each key is an author's name and the corresponding value is their affiliation. Returns None if the request fails or if an exception occurs.
    """

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        # Send a GET request to each URL
        page_response = requests.get(url)

        # Check if the request was successful
        if page_response.status_code == 200:
            page_soup = BeautifulSoup(page_response.content, 'html.parser')
            author_tags = page_soup.find_all('span', class_='loa__author-info')

            # Initialize a dictionary for the current paper's authors and affiliations
            authors_affiliations = {}
            authors_affiliations_countries = {}

            # Extract the text of each author and their affiliation
            for author in author_tags:
                author_name = author.find('span', class_='loa__author-name').text
                author_affiliation = author.find('span', class_='loa_author_inst').text.strip()
                authors_affiliations[author_name] = author_affiliation
            
            for author, affiliation in authors_affiliations.items():
                if ',' in affiliation:
                    # Split the string based on the last comma
                    split_affiliation = affiliation.rsplit(', ', 1)
                    authors_affiliations_countries[author] = {
                        'affiliation': split_affiliation[0].strip(),
                        'country': split_affiliation[1].strip()
                    }
                else:
                    # Handle cases where there is no comma
                    authors_affiliations_countries[author] = {
                        'affiliation': affiliation,
                        'country': None
                    }

            return authors_affiliations_countries
        else:
            print(f"Failed to fetch {url}, status code: {page_response.status_code}")
        
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return None

### TESTING ###
# url = 'https://doi.org/10.1145/3593013.3594084'
# response = requests.get(url)
# result = get_authors(response, url)
# print(result)