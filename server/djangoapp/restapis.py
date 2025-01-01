# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url',
    default="http://localhost:3030"
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """Perform a GET request to the backend."""
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    request_url = f"{backend_url}{endpoint}?{params}"

    print(f"GET from {request_url}")
    try:
        # Call the GET method of requests library with URL and parameters
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None


def analyze_review_sentiments(text):
    """Analyze sentiments of the given text using the sentiment analyzer."""
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    try:
        # Call the GET method of requests library with URL and parameters
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None


def post_review(data_dict):
    """Post a review to the backend."""
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None
