import csv
from authors import find_acm_paper
import requests
from bs4 import BeautifulSoup

# Initialize an empty list to store the titles
titles = []

# Open the CSV file
with open('icml2022.csv', mode='r', encoding='utf-8') as file:
    # Create a CSV reader
    csv_reader = csv.DictReader(file)
    
    # Iterate over each row in the CSV
    for row in csv_reader:
        # Extract the title and add it to the list
        titles.append(row['title'])

# titles now contains all the titles from the CSV file

def get_abstract(url):
    # Send a request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the blockquote with class 'abstract mathjax'
        abstract = soup.find('blockquote', class_='abstract mathjax')

        # Check if the abstract is found and has enough length
        if abstract and len(abstract.get_text(strip=True)) > 9:
            # Return the text of the abstract starting from the 9th index
            return abstract.get_text(strip=True)[9:]
        else:
            return "Abstract not found or too short."
    else:
        return "Failed to retrieve the webpage."

def get_authors(url):
    # Send a request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class 'authors'
        authors_div = soup.find('div', class_='authors')

        # Check if the authors div is found
        if authors_div:
            # Find all anchor tags within the authors div
            author_tags = authors_div.find_all('a')

            # Extract text from each anchor tag and add it to the authors list
            authors = [author.get_text(strip=True) for author in author_tags]

            return authors
        else:
            return "Authors section not found."
    else:
        return "Failed to retrieve the webpage."

def main():
  result = []

  for title in titles:
      url = find_acm_paper(title)
      abstract = get_abstract(url)
      authors = get_authors(url)

      paper_data = {
          'link': url if url else None,
          'title': title,
          'abstract': abstract if abstract else None,
          'author_names': authors if authors else None
      }

      print(paper_data)
      print()
      print()
              
      result.append(paper_data)
  
  write_dicts_to_csv(result, "output.csv")
            
def write_dicts_to_csv(dict_list, filename):
    # Open the file in write mode
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        writer = csv.DictWriter(file, fieldnames=dict_list[0].keys())

        # Write the header (column names)
        writer.writeheader()

        # Write each dictionary as a row in the CSV file
        for d in dict_list:
            writer.writerow(d)

# Example usage
main()