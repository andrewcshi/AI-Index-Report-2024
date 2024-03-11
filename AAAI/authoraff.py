import requests
import json
import time
from bs4 import BeautifulSoup
import pycountry
import pandas as pd
import csv
import os

country_list = [country.name for country in pycountry.countries]
country_list.append('US')
country_list.append('USA')
country_list.append('UK')

def append_to_csv(row_data, file_name='data.csv', header=['Title', 'Authors', 'Affiliations', 'Countries']):
    try:
        with open(file_name, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            file.seek(0, 2)
            if file.tell() == 0:
                writer.writerow(header)
            writer.writerow(row_data)
    except Exception as e:
        print(f"Error appending to CSV: {e}")

def get_last_processed_paper_from_csv(csv_file):
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            last_line = None
            for last_line in csv.reader(file): pass
            if last_line:
                return last_line[0]
    except FileNotFoundError:
        print(f"No CSV file found with the name {csv_file}. Starting from the beginning.")
        return None

def find_acm_paper(title, max_retries=3, delay=10):
    cse_id = os.environ.get("CSE_ID")
    api_key = os.environ.get("API_KEY")
    if not cse_id or not api_key:
        print("CSE ID or API key not found. Please set them as environment variables.")
        return None

    query = f"{title} site:acm.org"
    attempt = 0
    search_url = "https://www.googleapis.com/customsearch/v1"

    while attempt < max_retries:
        try:
            params = {'q': query, 'cx': cse_id, 'key': api_key, 'num': 1}
            response = requests.get(search_url, params=params)
            if response.status_code // 100 == 4:
                return None
            response.raise_for_status()
            search_results = json.loads(response.text)

            if 'items' in search_results and search_results['items']:
                top_result_url = search_results['items'][0]['link']
                if '/pdf' in top_result_url:
                    top_result_url = top_result_url.replace('/pdf', '')
                if '/epdf' in top_result_url:
                    top_result_url = top_result_url.replace('/epdf', '')
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

def get_authors(url):
    try:
        page_response = requests.get(url)

        if page_response.status_code == 200:
            page_soup = BeautifulSoup(page_response.content, 'html.parser')
            author_tags = page_soup.find_all('span', class_='loa__author-info')

            authors_affiliations = {}
            authors_affiliations_countries = {}

            for author in author_tags:
                author_name = author.find('span', class_='loa__author-name').text
                author_affiliation = author.find('span', class_='loa_author_inst').text.strip()
                authors_affiliations[author_name] = author_affiliation
            
            for author, affiliation in authors_affiliations.items():
                country_found = None

                for country in country_list:
                    if country in affiliation:
                        country_found = country
                        break

                authors_affiliations_countries[author] = {
                    'affiliation': affiliation,
                    'country': country_found
                }

            return authors_affiliations_countries
        else:
            print(f"Failed to fetch {url}, status code: {page_response.status_code}")
        
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return None

def write_keywords_to_csv(titles, output_file_name):
    last_processed_title = get_last_processed_paper_from_csv(output_file_name)
    start_processing = False if last_processed_title else True

    for title in titles:
        if title == last_processed_title:
            start_processing = True
            continue
        if not start_processing:
            continue

        time.sleep(8)
        paper_url = find_acm_paper(title)
        print(paper_url)

        if paper_url is None:
            append_to_csv([title, "", "", ""], output_file_name)
            print(f"400-level error or failure to find: {title}")
            continue

        response = requests.get(paper_url)
        webpage_content = response.text

        soup = BeautifulSoup(webpage_content, 'html.parser')

        citation_title_element = soup.find('h1', class_='citation__title')
        
        if citation_title_element:
            citation_title = citation_title_element.get_text()
        else:
            append_to_csv([title, "", "", ""], output_file_name)
            print(f"Citation title not found for: {title}")
            continue
        
        print(citation_title)
        print(title)

        if citation_title.lower() in title.lower() or title.lower() in citation_title.lower():
            authors_info = get_authors(paper_url)
            authors = list(authors_info.keys())
            affiliations = [info['affiliation'] for info in authors_info.values()]
            countries = [info.get('country') for info in authors_info.values() if info.get('country')]

            row_data = [title, str(authors), str(affiliations), str(countries)]
            append_to_csv(row_data, output_file_name)
            print(f"Processed: {title}")
        else:
            append_to_csv([title, [], [], []], output_file_name)


df = pd.read_csv('Completed AAAI Data/aaai2023.csv')
all_titles = list(df['title'])
write_keywords_to_csv(all_titles, 'data.csv')