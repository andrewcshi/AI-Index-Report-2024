from bs4 import BeautifulSoup
from abstracts20 import get_abstracts
import time

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

    with open(file, 'r') as facct_file:
        content = facct_file.read()
        soup = BeautifulSoup(content, 'lxml')
        div_tag = soup.find('div', class_='col-lg-12')
        papers = div_tag.find_all('a')
        for paper in papers:
            paper_lower = paper.text.lower()
            if 'acm.org' in paper['href']:  # Check if 'acm.org' is in href
                doi_link = paper['href']
                abstract = get_abstracts(doi_link)
                time.sleep(10)
                for keyword in keywords:
                    if abstract:
                        if keyword in paper_lower or keyword in abstract:  # Check if keyword match exists
                            papers_links[doi_link] = paper.text  # Store link and title in dictionary
                            print(papers_links)
                    else:
                        if keyword in paper_lower:  # Check if keyword match exists
                            papers_links[doi_link] = paper.text  # Store link and title in dictionary
                            print(papers_links)
    
    return papers_links

### TESTING ###
result = find_papers('faccthtml/facctpapers20.html', security_keywords)
print(result)
print(len(result))