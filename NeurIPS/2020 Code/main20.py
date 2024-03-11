import csv
from abstracts20 import get_abstract
from authors20 import get_authors
from keywords20 import get_keywords
from loadpapers import load_dictionary_at_index

# def remove_unwanted_part(original_dict):
#     updated_dict = {}
#     for key, value in original_dict.items():
#         # Replace the unwanted part from the key
#         new_key = key.replace('//virtual/2022/', '/')
#         updated_dict[new_key] = value
#     return updated_dict

def append_to_csv(data, file_name='data.csv'):
    """Append a single data entry to a CSV file."""
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data.values())

def get_last_processed_paper_from_csv(csv_file):
    """Retrieve the title of the last processed paper from the CSV file."""
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            last_line = None
            for last_line in csv.reader(file): pass
            if last_line:
                return last_line[2]  # Assuming the title is the third element in the row
    except FileNotFoundError:
        print(f"No CSV file found with the name {csv_file}. Starting from the beginning.")
        return None

def main():
    base_url = 'https://nips.cc/virtual/2020/papers.html?filter=titles'
    result = []

    # Define keyword lists
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
    
    # Modify keywords to lowercase for comparison purposes
    transparency_keywords = [keyword.lower() for keyword in transparency_keywords]
    fairness_keywords = [keyword.lower() for keyword in fairness_keywords]
    privacy_keywords = [keyword.lower() for keyword in privacy_keywords]
    security_keywords = [keyword.lower() for keyword in security_keywords]

    file_path = 'papers20.txt'
    papers_transparency = load_dictionary_at_index(file_path, 0)
    papers_fairness = load_dictionary_at_index(file_path, 1)
    papers_privacy = load_dictionary_at_index(file_path, 2)
    papers_security = load_dictionary_at_index(file_path, 3)

    # papers_transparency = remove_unwanted_part(papers_transparency)
    # papers_fairness = remove_unwanted_part(papers_fairness)
    # papers_privacy = remove_unwanted_part(papers_privacy)
    # papers_security = remove_unwanted_part(papers_security)

    # Determine the last processed paper
    last_processed_paper_title = get_last_processed_paper_from_csv('data.csv')

    # Set to True if no last processed paper is found
    start_processing = last_processed_paper_title is None

    if start_processing:
        # Initialize the CSV file with header if starting fresh
        with open('data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['link', 'category', 'title', 'abstract', 'keywords', 'author_names'])
            writer.writeheader()

    count = 1
    for paper_category in [papers_transparency, papers_fairness, papers_privacy, papers_security]:
        for paper in paper_category:
            if not start_processing and paper_category[paper] == last_processed_paper_title:
                start_processing = True
                continue

            if start_processing:
                link = paper

                abstract = get_abstract(link)
                keywords = get_keywords(link)
                authors = get_authors(link)

                # Construct the paper_data dictionary with the processed values.
                paper_data = {
                    'link': link,
                    'category': count,
                    'title': paper_category[paper],
                    'abstract': abstract if abstract else None,
                    'keywords': keywords if keywords else None,
                    'author_names': authors if authors else None,
                    # 'affiliations': affiliations,
                    # 'affiliated_countries': affiliated_countries
                }

                # paper_data = {
                #     'link': link,
                #     'category': count,
                #     'title': paper_category[paper],
                #     'abstract': abstract if abstract else None,
                #     'keywords': keywords if keywords else None,
                #     'author_names': list(authors.keys()) if authors.keys() else None,
                #     'affiliations': [data['affiliation'] for data in authors.values()] if authors else None,
                #     'affiliated_countries': [data['country'] for data in authors.values()] if authors else None
                # }

                print(paper_data)
                print()
                print()
                
                result.append(paper_data)
                append_to_csv(paper_data)

        count += 1
        print('Category finished')
        print()

    print(result)

if __name__ == "__main__":
    main()