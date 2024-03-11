import requests
from bs4 import BeautifulSoup

def get_keywords(response, url):
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
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    reference_number = url[16:]
    full_link = 'https://dl.acm.org/doi/fullHtml/' + reference_number
    url = full_link
    
    try:
        # Send a GET request to each URL
        page_response = requests.get(url)

        # Check if the request was successful
        if page_response.status_code == 200:
            page_soup = BeautifulSoup(page_response.content, 'html.parser')

            # Find the keywords using its unique identifier (e.g., class name)
            keywords = page_soup.find_all('span', class_='keyword')
            keyword_list = []
            for keyword in keywords:
                keyword_list.append(keyword.find('small').text)

            ccs_keyword = page_soup.find('div', class_='CCSconcepts')
            ccs_list = []
            # Check if ccs_keyword is not None before attempting to find all 'strong' tags
            if ccs_keyword:
                strong_tags = ccs_keyword.find_all('strong')
                ccs_list = [tag.text for tag in strong_tags]

            return keyword_list, ccs_list
        else:
            print(f"Failed to fetch {url}, status code: {page_response.status_code}")

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return None, None

### TESTING ###
# url = 'https://doi.org/10.1145/3593013.3594084'
# response = requests.get(url)
# result = get_keywords(response, url)
# print(result)