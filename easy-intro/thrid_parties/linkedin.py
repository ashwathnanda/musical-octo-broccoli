import os

import requests


def scrape_linkedin_profile(linkedin_profile_url: str) -> dict:
    # Your code here
    """
    scrape information from linkedin profiles,
    Manually scrape the information from the linkedin profile
    :param linkedin_profile_url: URL of the linkedin profile
    :return: dictionary of the information
    """
    # api_endpoint = "https://nublela.co/proxycurl/api/v2/linkedin"
    # TODO: Use the Proxycurl API to scrape the linkedin profile
    api_url = ("https://gist.githubusercontent.com/ashwathnanda/93539771e40fbc2cdd7e1f70f0e826c0/raw/376db6e3c0d6c7e20f044372be836c2b1c96f83d/proxy-curl-ashwath.json")
    header = {
        "Authorization": f"Bearer {os.environ.get('PROXYCURL_API_KEY')}"
    }

    # Make a request to the API
    response = requests.get(api_url)

    if response.status_code == 200:
        return _clean_linkedin_data(response.json())
    else:
        return {"error": "Failed to fetch the data"}


def _clean_linkedin_data(data):
    """
    clean the data from the linkedin profile
    :param data: dictionary of the linkedin profile
    :return: cleaned dictionary
    """
    cleaned_data = {
        key: value
        for key, value in data.items()
        if value and value not in (["", [], {}, None])
        and key not in ["people_also_viewed", "certifications"]
    }
    if "groups" in cleaned_data:
        for group in cleaned_data["groups"]:
            group.pop("profile_pic_url", None)

    return cleaned_data
