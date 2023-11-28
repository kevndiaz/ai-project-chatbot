import sys
import os
import requests


def main(dict):
    """
    Performs a Google Custom Search using the specified query and returns a link to the first result.

    Args:
        dict (dict): A dictionary containing the input parameters.

    Returns:
        dict: A dictionary containing the search result link.
    """

    # Google API credentials
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
    SEARCH_ENGINE_ID = os.environ['SEARCH_ENGINE_ID']

    # Construct the search query
    search_query = dict["textbook"] + ' pdf'

    # Google Custom Search API endpoint
    url = 'https://www.googleapis.com/customsearch/v1'

    # Set the parameters for the API request
    params = {
        'q': search_query,
        'key': GOOGLE_API_KEY,
        'cx': SEARCH_ENGINE_ID
    }

    # Make a request to the Google Custom Search API
    response = requests.get(url, params)
    results = response.json()

    # Check if the API response contains search results
    if 'items' in results:
        # Return the link to the first search result
        return {'message': results['items'][0]['link']}
