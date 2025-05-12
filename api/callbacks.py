from type_annotations.type_dicts import (
    OutputData,
    RoleData,
)

from typing import Callable


# Main Higher order function
def role_data_cb(schema: OutputData, callback: Callable[[RoleData], None]):
    """
    Apply some callback function to the role_data

    role_data - Represents the RoleData dict /type_annotations/type_dicts.py

    Args:
        schema: The output data structure
        callback: Some callback function that uses the role_data
    """
    companies = schema["companies"]

    for _, role in companies.items():
        for _, role_data in role.items():
            callback(role_data)


def sort_reviews(role_data: RoleData):
    """
    Sorts the reviews in descending order

    Args:
        role_schema: The output of what the data should look like
    """
    reviews = role_data["reviews"]
    reviews.sort(key=lambda data: data["rating"], reverse=True)


def calculate_statistics(role_data: RoleData):
    """
    Calculates the average pay and rating the reviews

    Args:
        role_data: The statistics of the position

    """

    review_list = role_data["reviews"]

    if review_list:
        role_data["avgPay"] = calc_avg(review_list, "pay")
        role_data["avgRating"] = calc_avg(review_list, "rating")


def calc_avg(review_list, key, precision=2):
    """
    Calculates the average given a dict of reviews, with the provided key

    Args:
        review_list: List of reviews for a position
        key: The part we want to calculate the average of
        precision: The rounding we want to use

    """
    total = sum(review[key] for review in review_list)
    return round((total / len(review_list)), precision)
