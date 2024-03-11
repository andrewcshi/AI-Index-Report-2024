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
            # Check if the h4 text matches "Abstract"
            if h4.text.strip().lower() == "abstract":
                # Find the next sibling that is a p tag
                next_p = h4.find_next_sibling('p')
                
                if next_p:
                    return next_p.text[:len(next_p.text) - 1]
                else:
                    return "No p tag follows the specified h4 tag."
        
        return "No h4 tag with the text 'Abstract' found."
    except requests.HTTPError as e:
        return f"HTTP Error: {e}"
    except requests.RequestException as e:
        return f"Error fetching URL: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

### TESTING ###
# url = 'https://nips.cc/virtual/2020/poster/17244'
# print(get_abstract(url))