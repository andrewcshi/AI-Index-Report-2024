import requests
from bs4 import BeautifulSoup

def get_keywords(url):
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
    
    try:
        # Fetch the HTML content from the initial URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
        html_content = response.text

        # Parse the initial HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the 'a' tag with title 'OpenReview'
        a_tag = soup.find('a', title='OpenReview')
        if not a_tag or 'href' not in a_tag.attrs:
            return "OpenReview link not found."

        # Follow the 'OpenReview' link
        open_review_url = a_tag['href']
        response = requests.get(open_review_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the <strong> tag with the specific class and text 'Keywords'
        strong_tag = soup.find(lambda tag: tag.name == "strong" and
                                            tag.get("class") == ["note-content-field", "disable-tex-rendering"] and
                                            "Keywords" in tag.text)

        # Initialize an empty list for keywords
        keywords = []

        if strong_tag:
            # Find the immediately following sibling <span> tag
            span_tag = strong_tag.find_next_sibling('span')

            if span_tag:
                # Extract text, split by ',', and strip whitespaces from each entry
                keywords = [keyword.strip() for keyword in span_tag.text.split(',')]

        return keywords
    except requests.HTTPError as e:
        return f"HTTP Error: {e}"
    except requests.RequestException as e:
        return f"Error fetching URL: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

### TESTING ###
# url = 'https://nips.cc/virtual/2023/poster/71051'
# result = get_keywords(url)
# print(result)