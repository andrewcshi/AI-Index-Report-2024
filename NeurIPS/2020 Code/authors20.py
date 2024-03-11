import requests
from bs4 import BeautifulSoup
import pycountry

country_list = [country.name for country in pycountry.countries]
country_list.append('US')
country_list.append('USA')
country_list.append('UK')

def get_authors(url):
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
    try:
        # Fetch the HTML content from the initial URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
        html_content = response.text

        # Parse the initial HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the 'a' tag with title 'OpenReview'
        a_tag = soup.find('a', class_='paper-pdf-link')
        if not a_tag or 'href' not in a_tag.attrs:
            return "Link not found."

        # Follow the 'OpenReview' link
        link = a_tag['href']
        response = requests.get(link)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all h4 tags
        h4_tags = soup.find_all('h4')
        
        for h4 in h4_tags:
            # Check if the h4 text matches "Authors"
            if h4.text.strip().lower() == "authors":
                # Find the next sibling that is a p tag
                next_p = h4.find_next_sibling('p')
                
                if next_p:
                    # Split the authors text by comma and strip whitespaces from each element
                    authors_list = [author.strip() for author in next_p.text.split(',')]
                    return authors_list
                else:
                    return "No p tag follows the specified h4 tag."
        
        return "No h4 tag with the text 'Authors' found."
    except requests.HTTPError as e:
        return f"HTTP Error: {e}"
    except requests.RequestException as e:
        return f"Error fetching URL: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

### TESTING ###
# url = 'https://nips.cc/virtual/2020/poster/17724'
# print(get_authors(url))