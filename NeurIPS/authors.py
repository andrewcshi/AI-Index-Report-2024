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
    # Fetch the HTML content from the initial URL
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the <h4> tag with the text "Abstract"
    abstract_h4 = soup.find('h4', string="Authors")

    if abstract_h4:
        # Initialize desired_p as None
        desired_p = None
        
        # Find the next sibling of <h4> that is a <p> tag
        next_sibling = abstract_h4.find_next_sibling('p')
        
        # Iterate through following siblings until a non-empty <p> tag is found
        while next_sibling:
            # Check if the <p> tag contains text
            if next_sibling.name == 'p' and next_sibling.text.strip():
                desired_p = next_sibling
                break
            # Move to the next sibling
            next_sibling = next_sibling.find_next_sibling('p')
        
        # Check if a non-empty <p> tag was found
        if desired_p:
            authors_list = [author.strip() for author in desired_p.text.split(',')]
            return authors_list
        else:
            return "No non-empty <p> tag found immediately following the 'Authors' <h4>."
    else:
        return "An <h4> tag with the text 'Authors' was not found."

### TESTING ###
# url = 'https://papers.nips.cc/paper_files/paper/2019/hash/56bd37d3a2fda0f2f41925019c81011d-Abstract.html'
# print(get_authors(url))