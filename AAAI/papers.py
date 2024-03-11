from bs4 import BeautifulSoup
import requests
import json
import time
from abstracts import get_abstracts
import os

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

    query = f"{title} site:arxiv.org"
    attempt = 0
    search_url = "https://www.googleapis.com/customsearch/v1"

    while attempt < max_retries:
        try:
            params = {
                'q': query,
                'cx': cse_id,
                'key': api_key,
                'num': 1
            }
            response = requests.get(search_url, params=params)
            response.raise_for_status()

            search_results = json.loads(response.text)

            if 'items' in search_results and search_results['items']:
                top_result_url = search_results['items'][0]['link']
                if '/pdf' in top_result_url:
                    top_result_url = top_result_url.replace('/pdf', '/abs')
                if '/html' in top_result_url:
                    top_result_url = top_result_url.replace('/html', '/abs')
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

def find_papers(file, transparency_keywords, fairness_keywords, privacy_keywords, security_keywords):
    papers_links_transparency = {}
    papers_links_fairness = {}
    papers_links_privacy = {}
    papers_links_security = {}

    with open(file, 'r') as aies_file:
      content = aies_file.read()
      soup = BeautifulSoup(content, 'lxml')
      papers = []

      title_spans = soup.find_all('span', class_='title')
      if title_spans:
          for span in title_spans:
              papers.append(span.get_text())

    for paper in papers[1:]:
      time.sleep(1)
      title = paper
      title_lower = paper.lower()
      link = find_acm_paper(title)
      abstract = get_abstracts(link)
      abstract_lower = abstract.lower() if abstract else None

      if abstract_lower == None:
        continue

      for keyword in transparency_keywords:
          if keyword in title_lower or keyword in abstract_lower:
            papers_links_transparency[link] = title

      for keyword in fairness_keywords:
          if keyword in title_lower or keyword in abstract_lower:
            papers_links_fairness[link] = title

      for keyword in privacy_keywords:
          if keyword in title_lower or keyword in abstract_lower:
            papers_links_privacy[link] = title

      for keyword in security_keywords:
          if keyword in title_lower or keyword in abstract_lower:
            papers_links_security[link] = title

    return papers_links_transparency, papers_links_fairness, papers_links_privacy, papers_links_security

### TESTING ###
# result = find_papers('aaai23.html', transparency_keywords, fairness_keywords, privacy_keywords, security_keywords)
# print(result)