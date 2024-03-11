from papers19 import find_papers
from abstracts19 import get_abstracts
from keywords19 import get_keywords
from authors19 import get_authors
import time
import requests
import csv

def main():
    base_url = 'https://facctconference.org/2019/acceptedpapers'
    result = []

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

    papers_transparency = find_papers('faccthtml/facctpapers19.html', transparency_keywords)
    papers_fairness = find_papers('faccthtml/facctpapers19.html', fairness_keywords)
    papers_privacy = find_papers('faccthtml/facctpapers19.html', privacy_keywords)
    papers_security = find_papers('faccthtml/facctpapers19.html', security_keywords)

    for paper_category in [papers_transparency, papers_fairness, papers_privacy, papers_security]:
        for paper in paper_category:
            doi_link = paper
            try:
              response = requests.get(doi_link)
            except:
              continue

            abstract = get_abstracts(doi_link)
            time.sleep(10)
            keywords = get_keywords(response, doi_link)
            time.sleep(10)
            authors = get_authors(response, doi_link)

            paper_data = {
                'doi_link': paper,
                'title': paper_category[paper],
                'abstract': abstract,
                'keywords': keywords[0],
                'CCS concepts': keywords[1],
                'author_names': list(authors.keys()),
                'affiliations': [data['affiliation'] for data in authors.values()],
                'affiliated_countries': [data['country'] for data in authors.values()]
            }

            print(paper_data)
            print()
            print()
            
            result.append(paper_data)

            time.sleep(10)
      
        print('Category finished')
        print()

    print(result)
    
    keys = result[0].keys()
    with open('data.csv', 'w', newline='') as output_file:
      dict_writer = csv.DictWriter(output_file, keys)
      dict_writer.writeheader()
      dict_writer.writerows(result)

if __name__ == "__main__":
    main()