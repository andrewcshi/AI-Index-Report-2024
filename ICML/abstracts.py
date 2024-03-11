import requests
from bs4 import BeautifulSoup

def get_abstract(url):
    """
    Fetches and returns the text from a div with id 'abstractExample' from the given URL.

    Parameters:
    url (str): URL of the webpage to fetch.

    Returns:
    str: Text content of the div with id 'abstractExample', or an error message if not found.
    """
    try:
        # Send a request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the div with id 'abstractExample'
            abstract_div = soup.find('div', id='abstractExample')

            # Check if the div is found
            if abstract_div:
                text = abstract_div.get_text(strip=True)
                return text[9:] if 'Abstract:' in text else text
            else:
                return "Abstract not found."
        else:
            return "Failed to retrieve webpage. Status code: " + str(response.status_code)

    except requests.RequestException as e:
        return f"An error occurred: {e}"

### TESTING ###
# url = 'https://icml.cc/virtual/2023/poster/25050'
# print(get_abstract(url))