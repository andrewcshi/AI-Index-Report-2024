import csv
import pandas as pd
from keywords20 import get_keywords
import time

# Load the CSV file
df = pd.read_csv('Completed Data/data2022.csv')

# Grab a specific column, for example 'ColumnName'
column_data = df['link']

# Now, column_data contains the data of the specified column
print(column_data)

def write_keywords_to_csv(urls, output_file_name):
    """
    Fetches keywords from a list of URLs and writes them to a CSV file.

    Parameters:
    urls (list of str): A list of URLs to fetch keywords from.
    output_file_name (str): The name of the output CSV file.

    """
    # Open the CSV file for writing
    with open(output_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['URL', 'Keywords'])

        # Loop through each URL
        for url in urls:
            time.sleep(1)
            # Fetch keywords for the current URL
            keywords = get_keywords(url)
            print('Executed.')
            # Check if keywords is a list, indicating successful extraction
            # if isinstance(keywords, list):
            #     # Join the list of keywords into a single string
            #     keywords_str = keywords
            # else:
            #     # If keywords is not a list, something went wrong; log the error message instead
            keywords_str = keywords

            # Write the URL and the keywords (or error message) to the CSV file
            writer.writerow([url, keywords_str])

write_keywords_to_csv(column_data, '2022keywords.csv')