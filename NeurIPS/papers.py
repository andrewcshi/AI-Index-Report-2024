from bs4 import BeautifulSoup
from abstracts import get_abstract


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

def find_papers(file, transparency_keywords, fairness_keywords, privacy_keywords, security_keywords):
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
    papers_links_transparency = {}
    papers_links_fairness = {}
    papers_links_privacy = {}
    papers_links_security = {}

    with open(file, 'r') as neurips_file:
      content = neurips_file.read()
      soup = BeautifulSoup(content, 'lxml')

      ul_tag = soup.find('ul', class_='paper-list')
      # Find all <a> tags within <li class="none">
      li_tags = ul_tag.find_all('li', class_='conference')
      # Extract just the <a> tags from those <li> elements
      papers = [li.find('a') for li in li_tags]

    for paper in papers:
      title = paper.text.strip()
      title_lower = title.lower()
      link = 'https://papers.nips.cc' + paper['href']
      abstract = get_abstract(link)
      abstract_lower = abstract.lower()

      for keyword in transparency_keywords:
          if keyword in title_lower or keyword in abstract_lower: # Check if keyword match exists
            papers_links_transparency[link] = title # Store link and title in dictionary
            print('Executed')

      for keyword in fairness_keywords:
          if keyword in title_lower or keyword in abstract_lower: # Check if keyword match exists
            papers_links_fairness[link] = title # Store link and title in dictionary

      for keyword in privacy_keywords:
          if keyword in title_lower or keyword in abstract_lower: # Check if keyword match exists
            papers_links_privacy[link] = title # Store link and title in dictionary

      for keyword in security_keywords:
          if keyword in title_lower or keyword in abstract_lower: # Check if keyword match exists
            papers_links_security[link] = title # Store link and title in dictionary

    return papers_links_transparency, papers_links_fairness, papers_links_privacy, papers_links_security

### TESTING ###
result = find_papers('neurips22.html', transparency_keywords, fairness_keywords, privacy_keywords, security_keywords)
print(result)