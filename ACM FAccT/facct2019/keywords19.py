import requests
from bs4 import BeautifulSoup

def get_keywords(response, url):  
    soup = BeautifulSoup(response.content, 'html.parser')
    reference_number = url[16:]
    full_link = 'https://dl.acm.org/doi/fullHtml/' + reference_number
    url = full_link

    try:
        page_response = requests.get(url)

        if page_response.status_code == 200:
            page_soup = BeautifulSoup(page_response.content, 'html.parser')

            keywords = page_soup.find_all('span', class_='keyword')
            keyword_list = []
            for keyword in keywords:
                keyword_list.append(keyword.find('small').text)

            ccs_keyword = page_soup.find('div', class_='CCSconcepts')
            ccs_list = []
            if ccs_keyword:
                strong_tags = ccs_keyword.find_all('strong')
                ccs_list = [tag.text for tag in strong_tags]

            return keyword_list, ccs_list
        else:
            print(f"Failed to fetch {url}, status code: {page_response.status_code}")

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return None, None

### TESTING ###
# url = 'https://doi.org/10.1145/3593013.3594084'
# response = requests.get(url)
# result = get_keywords(response, url)
# print(result)