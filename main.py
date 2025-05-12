import json
from typing import Any

import requests
from api.api_processor import format_data
from type_annotations.type_dicts import InputData, OutputData


def fetch_data(url: str) -> InputData:
    """
    Fetch data from the API

    Args:
        url: The API URL

    Returns:
        The parsed JSON response
    """
    response = requests.get(url)
    return response.json()


def post_data(url: str, data: OutputData) -> str:
    """
    Submit processed data to the API

    Args:
        url: The API URL
        data: The processed data to submit

    Returns:
        Response information
    """
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    return f"Status Code: {response.status_code}\n Message: {response.text}"


def run(url: str):
    """
    Main function to format and send the formatted data back to the API

    Args:
        url: The API URL
    """
    try:
        input_data = fetch_data(url)
        print("Retrieved data from API")

        formatted_data = format_data(input_data)
        print("Formatted the data")

        result = post_data(url, formatted_data)

        print(result)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    run("API")
