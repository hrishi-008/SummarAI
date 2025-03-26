"""
Website Content Scraper Module.

This module handles the extraction of content from websites listed in the search results.
It performs the following functions:
1. Reads search results from 'gsearch_results.json'
2. For each URL in the results:
   - Makes an HTTP request to fetch the webpage
   - Parses the HTML content using BeautifulSoup
   - Extracts the main text content
   - Cleans and formats the text
3. Saves the scraped content to a JSON file

The module includes error handling for:
- Access denied websites
- Invalid URLs
- Malformed HTML content

Output:
    Saves scraped content to 'searchResults/scraped_data.json' in the format:
    {
        'query': str,
        'results': [
            {
                'title': str,
                'link': str,
                'text': str
            },
            ...
        ]
    }

Dependencies:
    - requests: For HTTP requests
    - beautifulsoup4: For HTML parsing
    - json: For data storage

Author: Hrishikesh
Date: March 2024
"""

import json
import requests
from bs4 import BeautifulSoup as bs

def parse_search_results():
    """
    Parses the search results from a JSON file and scrapes the content of each link.
    Returns:
        None
    Raises:
        FileNotFoundError: If the JSON file containing the search results is not found.
    """
    # read results.json
    with open('searchResults/gsearch_results.json', 'r') as f:
        results = json.load(f)

    query = results['query']

    variable = {
        'query': query,
        'results': []
    }


    for i in results['results']:
        title = i['title']
        link = i['link']
        content = requests.get(link).text
        soup = bs(content, 'html.parser')
        body = soup.find('body')
        # print(body)
        try:
            text = body.get_text().strip()
            # remove unnecessary characters from the text including newlines and extra spaces
            text = ' '.join(text.split())

        except:
            text = 'Access Denied'
        #  save the results to a json variable
        variable['results'].append({'title': title, 'link': link, 'text': text})
    # Save the results to a json file
    with open('searchResults/scraped_data.json', 'w') as f:
        json.dump(variable, f)

def main():
    parse_search_results()

if __name__ == '__main__':
    main()
