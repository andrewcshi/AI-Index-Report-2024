import csv
from data import get_data

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

    html_file_path = 'ICLR/iclrworkshop18.html'
    papers_transparency = get_data(html_file_path, transparency_keywords)
    papers_fairness = get_data(html_file_path, fairness_keywords)
    papers_privacy = get_data(html_file_path, privacy_keywords)
    papers_security = get_data(html_file_path, security_keywords)

    paper_categories = ['Transparency & Explainability', 'Fairness & Bias', 'Privacy & Data Governance', 'Security']

    # Determine the last processed paper
    last_processed_paper_title = get_last_processed_paper_from_csv('data.csv')

    # Set to True if no last processed paper is found
    start_processing = last_processed_paper_title is None

    if start_processing:
        # Initialize the CSV file with header if starting fresh
        with open('data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['link', 'category', 'title', 'author_names'])
            writer.writeheader()

    index = 0
    for paper_category in [papers_transparency, papers_fairness, papers_privacy, papers_security]:
        for paper in paper_category:
            if not start_processing and paper_category[paper] == last_processed_paper_title:
                start_processing = True
                continue

            if start_processing:
                link = paper

                # Construct the paper_data dictionary with the processed values.
                paper_data = {
                    'link': link,
                    'category': paper_categories[index],
                    'title': paper_category[paper][0],
                    'abstract': paper_category[paper][1],
                    'author_names': paper_category[paper][2]
                }

                print(paper_data)
                print()
                print()
                
                result.append(paper_data)
                append_to_csv(paper_data)

        index += 1
        print('Category finished')
        print()

    print(result)

if __name__ == "__main__":
    main()