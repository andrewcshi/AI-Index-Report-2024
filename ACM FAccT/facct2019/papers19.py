from bs4 import BeautifulSoup
from abstracts19 import get_abstracts
import time

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

def find_papers(file, keywords):
  papers_links = {}

  with open(file, 'r') as facct_file:
    content = facct_file.read()
    soup = BeautifulSoup(content, 'lxml')
    div_tag = soup.find('div', class_='col-lg-12')
    papers = div_tag.find_all('a')
    for paper in papers:
      paper_lower = paper.text.lower()
      doi_link = paper['href']
      abstract = get_abstracts(doi_link)
      time.sleep(10)
      for keyword in keywords:
        if abstract:
          if keyword in paper_lower or keyword in abstract:
            papers_links[doi_link] = paper.text
            print(papers_links)
        else:
          if keyword in paper_lower:
            papers_links[doi_link] = paper.text
            print(papers_links)
      
  return papers_links

### TESTING ###
# result = find_papers('faccthtml/facctpapers19.html', security_keywords)
# print(result)