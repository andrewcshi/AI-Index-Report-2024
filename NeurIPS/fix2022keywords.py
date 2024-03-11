import csv
import pandas as pd
import time
from bs4 import BeautifulSoup
from keywords import get_keywords

# Load the CSV file
df = pd.read_csv('Completed NeurIPS Data/data2022.csv')

def get_link(file_path, title):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <a> tags in the HTML with href containing '/virtual/2022'
    matching_links = soup.find_all('a', href=lambda href: href and '/virtual/2022' in href)
    
    for link in matching_links:
        link_text = link.get_text(strip=True)
        if title.lower() in link_text.lower():
            return 'https://nips.cc' + link['href']

    return None

def write_keywords_to_csv(titles, file_path, output_file_name):
    """
    Fetches keywords from a list of URLs and writes them to a CSV file.

    Parameters:
    urls (list of str): A list of URLs to fetch keywords from.
    output_file_name (str): The name of the output CSV file.

    """
    with open(output_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'URL', 'Keywords'])

        for title in titles:
            # Example URL fetching based on title, adjust this to your actual method
            url = get_link(file_path, title)  # Placeholder function, replace with actual logic to fetch URL

            # Fetch keywords for the current URL
            keywords = get_keywords(url)  # Placeholder function, replace with actual logic to fetch keywords

            # Write the title, URL, and keywords to the CSV file
            writer.writerow([title, url, keywords])
            print('Executed.')

write_keywords_to_csv(df['title'], 'neurips22keywords.html', '2022keywords.csv')