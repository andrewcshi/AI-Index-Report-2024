import requests
from bs4 import BeautifulSoup
import pycountry
import time
import json
import os

country_list = [country.name for country in pycountry.countries]
country_list.append('US')
country_list.append('USA')
country_list.append('UK')

def find_acm_paper(title):
    cse_id = os.environ.get("CSE_ID")
    api_key = os.environ.get("API_KEY")
    if not cse_id or not api_key:
        print("CSE ID or API key not found. Please set them as environment variables.")
        return None

    query = f"{title} site:arxiv.org"  # Keeping the site filter
    search_url = "https://www.googleapis.com/customsearch/v1"

    try:
        params = {
            'q': query,
            'cx': cse_id,
            'key': api_key,
            'num': 1  # Fetching only the top result
        }
        response = requests.get(search_url, params=params)
        response.raise_for_status()

        search_results = json.loads(response.text)

        if 'items' in search_results and search_results['items']:
            top_result_url = search_results['items'][0]['link']
            # # Check if '/pdf' is in the URL and remove it
            # if '/pdf' in top_result_url:
            #     top_result_url = top_result_url.replace('/pdf', '')
            return top_result_url
        else:
            print("No items found in the API response.")
            return None
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"Error occurred with Google Custom Search API: {e}")

    print("Failed to find the paper.")
    return None

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
                # Initialize country as None
                country_found = None

                # Check if any country is in the affiliation string
                for country in country_list:
                    if country in affiliation:
                        country_found = country
                        break  # Stop searching once a country is found

                if country_found:
                    # Replace the country and strip whitespaces
                    new_affiliation = affiliation.replace(country_found, '').strip()
                    # Remove the last character if the new string is not empty
                    affiliation_without_country = new_affiliation[:-1] if new_affiliation else new_affiliation
                else:
                    # Leave the affiliation as it is
                    affiliation_without_country = affiliation


                # Update the dictionary
                authors_affiliations_countries[author] = {
                    'affiliation': affiliation_without_country,
                    'country': country_found
                }

            return authors_affiliations_countries
        else:
            print(f"Failed to fetch {url}, status code: {page_response.status_code}")
        
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return None

### TESTING ###
# paper_title = "Adaptive Whitening in Neural Populations with Gain-modulating Interneurons"
# url = find_acm_paper(paper_title)
# response = requests.get(url)
# result = get_authors(response, url)
# print(result)