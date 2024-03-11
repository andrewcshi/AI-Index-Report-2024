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
  # Dictionary to store link-paper key-value pairs
  papers_links_transparency = {}
  papers_links_fairness = {}
  papers_links_privacy = {}
  papers_links_security = {}

  with open(file, 'r') as f:
      content = f.read()
      soup = BeautifulSoup(content, 'lxml')

      # Find all div tags with class 'maincard narrower poster'
      posters = soup.find_all('div', class_='maincard narrower poster')

      for poster in posters:
          # Find the div tag within the poster with class 'maincardBody'
          paper_div = poster.find('div', class_='maincardBody')
          if paper_div:
              title = paper_div.text.strip()
              title_lower = title.lower()

          # Find the a tag within the poster with title 'PDF'
          pdf_link = poster.find('a', title='PDF')
          if pdf_link:
              link = pdf_link['href']

          abstract = get_abstract(link)
          abstract_lower = abstract.lower()

          for keyword in transparency_keywords:
              if keyword in title_lower or keyword in abstract_lower: # Check if keyword match exists
                papers_links_transparency[link] = title # Store link and title in dictionary

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
# result = find_papers('iclrpapers20.html', security_keywords)
# print(result)