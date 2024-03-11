import requests
from bs4 import BeautifulSoup

def get_authors(response, url):
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
                if ',' in affiliation:
                    split_affiliation = affiliation.rsplit(', ', 1)
                    authors_affiliations_countries[author] = {
                        'affiliation': split_affiliation[0].strip(),
                        'country': split_affiliation[1].strip()
                    }
                else:
                    authors_affiliations_countries[author] = {
                        'affiliation': affiliation,
                        'country': None
                    }

            return authors_affiliations_countries
        else:
            print(f"Failed to fetch {url}, status code: {page_response.status_code}")
        
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return None

### TESTING ###
# url = 'https://doi.org/10.1145/3593013.3594084'
# response = requests.get(url)
# result = get_authors(response, url)
# print(result)