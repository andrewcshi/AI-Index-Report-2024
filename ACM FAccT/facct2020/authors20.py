import requests
from bs4 import BeautifulSoup
import pycountry

country_list = [country.name for country in pycountry.countries]
country_list.append('US')
country_list.append('UK')

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
                country_found = None

                for country in country_list:
                    if country in affiliation:
                        country_found = country
                        break

                if country_found:
                    new_affiliation = affiliation.replace(country_found, '').strip()
                    affiliation_without_country = new_affiliation[:-1] if new_affiliation else new_affiliation
                else:
                    affiliation_without_country = affiliation

                authors_affiliations_countries[author] = {
                    'affiliation': affiliation_without_country,
                    'country': country_found
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