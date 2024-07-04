import os

import requests


def scrape_linkedin_profile(linkedin_profile_url: str, **kwargs) -> dict:
    """
    scrape information from linkedin profiles,
    Manually scrape the information from the linkedin profile
    :param linkedin_profile_url: URL of the linkedin profile
    :return: dictionary of the information
    """

    print(linkedin_profile_url)

    if kwargs.get("mock"):
        api_url = "https://gist.githubusercontent.com/ashwathnanda/a8da1ec776a665f58d2141ff61ce3c1f/raw/78090f9714e83d11f66cc5cc1149bdda36f1c9bb/riya-verma-linkedin.json"
        header = {}

    else:
        api_url = "https://nubela.co/proxycurl//api/v2/linkedin"
        header = {"Authorization": f"Bearer {os.environ.get('PROXY_CURL_TOKEN')}"}

    # Make a request to the API
    response = requests.get(
        api_url, params={"url": linkedin_profile_url}, headers=header
    )

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
        if value
        and value not in (["", [], {}, None])
        and key not in ["people_also_viewed", "certifications"]
    }
    if "groups" in cleaned_data:
        for group in cleaned_data["groups"]:
            group.pop("profile_pic_url", None)

    return cleaned_data
