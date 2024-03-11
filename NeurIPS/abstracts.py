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
    # Fetch the HTML content from the initial URL
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the <h4> tag with the text "Abstract"
    abstract_h4 = soup.find('h4', string="Abstract")

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
            abstract_text = desired_p.text.replace('\n', '')
            return abstract_text
        else:
            return "No non-empty <p> tag found immediately following the 'Abstract' <h4>."
    else:
        return "An <h4> tag with the text 'Abstract' was not found."

### TESTING ###
# url = 'https://papers.nips.cc/paper_files/paper/2019/hash/00e26af6ac3b1c1c49d7c3d79c60d000-Abstract.html'
# print(get_abstract(url))