from bs4 import BeautifulSoup
import requests
import json
import time
from bs4.element import NavigableString
from abstracts import get_abstracts
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

def find_acm_paper(title, max_retries=3, delay=10):
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
            delay *= 2  # Exponential backoff
            attempt += 1

    print("Failed to find the paper after several attempts.")
    return None

def find_papers(file, keywords):
    """
    Searches an HTML file for academic papers that contain specific keywords in different categories.
    This function parses the file and extracts the link and title of the paper in key-value pairs.

    Parameters:
    file (str): The path to the HTML file to be parsed.
    keywords (list of str): A list of keyword strings to search within the papers' text.

    Returns:
    papers_links = A dictionary where each key is the DOI link and the value is the title of the paper.
    """

    # Dictionary to store link-paper key-value pairs
    papers_links = {}

    with open(file, 'r') as aies_file:
      content = aies_file.read()
      soup = BeautifulSoup(content, 'lxml')
      # Initialize a list to store texts
      papers = []

      entry_content_div = soup.find('div', class_='entry-content')
      # Check if the div was found
      if entry_content_div:
          # Find all strong tags within the div
          strong_tags = entry_content_div.find_all('strong')

          # Extract the text from each strong tag and add it to the list
          for tag in strong_tags:
              papers.append(tag.get_text())
      
      print(papers)

    for paper in papers:
      title = paper
      title_lower = paper.lower()
      link = find_acm_paper(title)
      print(link)
      abstract = get_abstracts(link)
      abstract_lower = abstract.lower() if abstract else None

      if abstract_lower == None:
        continue

      for keyword in keywords:
          if keyword in title_lower or keyword in abstract_lower: # Check if keyword match exists
            papers_links[link] = title # Store link and title in dictionary
            print('Executed')

    return papers_links

### TESTING ###
# result = find_papers('aies18.html', security_keywords)
# print(result)