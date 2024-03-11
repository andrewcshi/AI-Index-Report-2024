from bs4 import BeautifulSoup
import requests
import json
import time
import os

# Define keywords for each category as provided
transparency_keywords = [
  'Algorithmic Transparency',
  'Explainable AI',
  'Explainable Artificial Intelligence',
  'XAI',
  'Interpretability',
  'Model Explainability',
  'Explainability',
  'Transparency',
  'Human-understandable decisions',
  'Audit',
  'Auditing',
  'Outcome explanation',
  'Causality',
  'Causal reasoning',
  'Interpretable models',
  'Explainable models'
]
fairness_keywords = [
  'Algorithmic Fairness',
  'Bias Detection',
  'Bias',
  'Discrimination',
  'Fair ML',
  'Fair Machine Learning',
  'Unfairness',
  'Unfair',
  'Ethical algorithm design',
  'Bias mitigation',
  'Representational fairness',
  'Group fairness',
  'Individual fairness',
  'Fair data practices',
  'Equity in AI',
  'Equity in Artificial Intelligence',
  'Justice',
  'Non-discrimination'
]
privacy_keywords = [
  'Data privacy',
  'Data governance',
  'Differential privacy',
  'Data protection',
  'Data breach',
  'Secure data storage',
  'Data ethics',
  'Data integrity',
  'Data transparency',
  'Privacy by design',
  'Confidentiality',
  'Inference privacy',
  'Machine unlearning',
  'Privacy-preserving',
  'Data protection',
  'Anonymity',
  'Trustworthy data curation'
]
security_keywords = [
  'Red teaming',
  'Adversarial attack',
  'Cybersecurity',
  'Threat detection',
  'Vulnerability assessment',
  'Ethical hacking',
  'Fraud detection',
  'Security ethics',
  'AI incident',
  'Artificial Intelligence incident',
  'Security',
  'Safety',
  'Audits',
  'Attacks',
  'Forensic analysis',
  'Adversarial learning'
]

# Convert keywords to lowercase for searching purposes
transparency_keywords = [keyword.lower() for keyword in transparency_keywords]
fairness_keywords = [keyword.lower() for keyword in fairness_keywords]
privacy_keywords = [keyword.lower() for keyword in privacy_keywords]
security_keywords = [keyword.lower() for keyword in security_keywords]

def find_arxiv_paper(title, max_retries=3, delay=10):
    cse_id = os.environ.get("CSE_ID")
    api_key = os.environ.get("API_KEY")
    if not cse_id or not api_key:
        print("CSE ID or API key not found. Please set them as environment variables.")
        return None

    query = f"{title} site:arxiv.org"  # Keeping the site filter
    attempt = 0
    search_url = "https://www.googleapis.com/customsearch/v1"

    while attempt < max_retries:
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
                # Check if '/pdf' is in the URL and remove it
                if '/pdf' in top_result_url:
                    top_result_url = top_result_url.replace('/pdf', '/abs')
                    top_result_url = top_result_url.replace('.pdf', '')
                if '/html' in top_result_url:
                    top_result_url = top_result_url.replace('/html', '/abs')
                    top_result_url = top_result_url.replace('v1', '')
                return top_result_url
            else:
                print("No items found in the API response.")
                return None
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"Error occurred with Google Custom Search API: {e}")
            print(f"Retrying in {delay} seconds.")
            time.sleep(delay)
            delay *= 2
            attempt += 1

    print("Failed to find the paper after several attempts.")
    return None

def get_abstract(title):
    url = find_arxiv_paper(title)
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the blockquote tag with class 'abstract mathjax'
            blockquote_tag = soup.find('blockquote', class_='abstract mathjax')
            
            # Return the text within the blockquote tag if found
            if blockquote_tag:
                return blockquote_tag.text.strip()
            else:
                print("The specified tag was not found in the HTML content.")
                return None
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_data(html_file_path, keywords):
    """
    Reads an HTML file, parses its content to find all <a> tags within <div> tags with a specific class,
    and returns a dictionary where each key is the href of an <a> tag and its value is the text within the <a> tag.

    Parameters:
    - html_file_path (str): The file path to the HTML file.

    Returns:
    - dict: A dictionary with hrefs as keys and text content as values.
    """
    
    # Initialize an empty dictionary to hold the results
    papers_links = {}

    # Open and read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

        # Initialize BeautifulSoup to parse the provided HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all div tags with class 'displaycards touchup-date'
        divs = soup.find_all('div', class_='displaycards touchup-date')

        # Iterate through each div found
        for div in divs:
            # Within each div, find an a tag with class 'small-title text-underline-hover'
            a_tag = div.find('a', class_='small-title')
            if a_tag:
              title = a_tag.text.strip()
              link = 'https://iclr.cc' + a_tag['href']

            # Find abstract
            abstract = get_abstract(title)
            if abstract:
              abstract = abstract.replace('Abstract:', '').strip()

            # Find authors
            authors_div = div.find('div', class_='author-str')
            authors_list = []
            if authors_div:
                # Split the authors string into a list based on the delimiter
                authors_list = [author.strip() for author in authors_div.text.split('·')]

            for keyword in keywords:
                if abstract:
                    if keyword in title.lower() or keyword in abstract.lower():  # Check if keyword match exists in either title or abstract
                        papers_links[link] = [title, abstract, authors_list]  # Store link and title in dictionary
                        print('Executed.')
                elif keyword in title.lower():
                    papers_links[link] = [title, abstract, authors_list]  # Store link and title in dictionary
                    print('Executed.')

    return papers_links

### TESTING ###
# html_file_path = 'NeurIPS/neuripsworkshop22.html'
# papers_dict = get_data(html_file_path, transparency_keywords)
# print(papers_dict)