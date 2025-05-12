import pytest
from copy import deepcopy

from api.callbacks import sort_reviews, calculate_statistics, role_data_cb

from api.api_processor import (
    initialize_schema,
    map_user_ids_to_names,
    find_role_location,
    add_reviews_to_roles,
    format_data,
)


class TestInitializeSchema:
    def test_initialize_schema(self, input_data):
        result = initialize_schema(input_data["roles"])

        assert "Amazon" in result["companies"]
        assert "Apple" in result["companies"]
        assert "Meta" in result["companies"]

        amazon_dev = result["companies"]["Amazon"]["Software Developer"]
        assert amazon_dev["name"] == "Software Developer"
        assert amazon_dev["id"] == 25
        assert amazon_dev["avgPay"] == 0.00
        assert amazon_dev["avgRating"] == 0.00
        assert amazon_dev["reviews"] == []

    def test_initialize_schema_with_empty_roles(self):
        result = initialize_schema([])
        assert result["companies"] == {}

    def test_initialize_schema_with_duplicate_companies(self):
        roles = [
            {"role": "Developer", "roleId": 1, "company": "Google"},
            {"role": "Designer", "roleId": 2, "company": "Google"},
        ]

        result = initialize_schema(roles)

        assert "Google" in result["companies"]
        assert "Developer" in result["companies"]["Google"]
        assert "Designer" in result["companies"]["Google"]


def test_map_user_ids_to_names(input_data):
    result = map_user_ids_to_names(input_data)

    assert result[0] == "Sarah Zhang"
    assert result[1] == "Rishi Kanabar"
    assert result[2] == "Christine Cho"


class TestFindRoleLocation:
    def test_find_existing_role(self, expected_output_data):
        schema = deepcopy(expected_output_data)

        role_25 = find_role_location(schema, 25)
        assert role_25 is not None
        assert role_25["name"] == "Software Developer"

        role_114 = find_role_location(schema, 114)
        assert role_114 is not None
        assert role_114["name"] == "UX Designer"

    def test_find_role_empty_schema(self):
        empty_schema = {"companies": {}}
        role = find_role_location(empty_schema, 25)
        assert role is None


class TestAddReviewsToRoles:
    def test_add_reviews_to_roles(self, input_data):
        schema = initialize_schema(input_data["roles"])

        add_reviews_to_roles(schema, input_data)

        amazon_dev = schema["companies"]["Amazon"]["Software Developer"]
        assert len(amazon_dev["reviews"]) == 1
        assert amazon_dev["reviews"][0]["user"] == "Sarah Zhang"
        assert amazon_dev["reviews"][0]["rating"] == 1
        assert amazon_dev["reviews"][0]["pay"] == 38
        assert amazon_dev["reviews"][0]["review"] == 9935

        apple_designer = schema["companies"]["Apple"]["UX Designer"]
        assert len(apple_designer["reviews"]) == 2

    def test_add_reviews_to_roles_with_invalid_role_id(self, input_data):
        schema = initialize_schema(input_data["roles"])

        invalid_data = deepcopy(input_data)
        invalid_data["reviews"].append(
            {
                "roleId": 999,
                "ratingId": 1234,
                "overallScore": 5,
                "hourlyPay": 50,
                "userId": 0,
            }
        )

        add_reviews_to_roles(schema, invalid_data)

        amazon_dev = schema["companies"]["Amazon"]["Software Developer"]
        assert len(amazon_dev["reviews"]) == 1

    def test_add_reviews_to_roles_with_empty_data(self):
        schema = {
            "companies": {
                "Sandbox": {
                    "SWE": {
                        "name": "SWE",
                        "id": 1,
                        "avgPay": 0.0,
                        "avgRating": 0.0,
                        "reviews": [],
                    }
                }
            }
        }
        empty_data = {"reviews": [], "users": []}

        add_reviews_to_roles(schema, empty_data)

        assert schema["companies"]["Sandbox"]["SWE"]["reviews"] == []


class TestCallbacks:
    def test_role_data_cb_sort_reviews(self, expected_output_data):
        schema = deepcopy(expected_output_data)

        apple_reviews = schema["companies"]["Apple"]["UX Designer"]["reviews"]
        apple_reviews[0], apple_reviews[1] = apple_reviews[1], apple_reviews[0]

        role_data_cb(schema, sort_reviews)

        sorted_reviews = schema["companies"]["Apple"]["UX Designer"]["reviews"]
        assert sorted_reviews[0]["rating"] == 2
        assert sorted_reviews[1]["rating"] == 1

    def test_role_data_cb_calculate_statistics(self):
        schema = {
            "companies": {
                "Sandbox": {
                    "SWE": {
                        "name": "SWE",
                        "id": 1,
                        "avgPay": 0.0,
                        "avgRating": 0.0,
                        "reviews": [
                            {"user": "User1", "rating": 4, "pay": 20, "review": 1},
                            {"user": "User2", "rating": 2, "pay": 30, "review": 2},
                        ],
                    }
                }
            }
        }

        role_data_cb(schema, calculate_statistics)

        role = schema["companies"]["Sandbox"]["SWE"]
        assert role["avgPay"] == 25.00
        assert role["avgRating"] == 3.00


class TestProcessData:
    def test_process_data_complete(self, input_data, expected_output_data):
        result = format_data(input_data)

        assert "companies" in result
        assert len(result["companies"]) == 3
        assert "Amazon" in result["companies"]
        assert "Apple" in result["companies"]
        assert "Meta" in result["companies"]

        apple_ux = result["companies"]["Apple"]["UX Designer"]
        assert apple_ux["avgPay"] == 29.00
        assert apple_ux["avgRating"] == 1.50
        assert len(apple_ux["reviews"]) == 2

        assert apple_ux["reviews"][0]["rating"] == 2
        assert apple_ux["reviews"][1]["rating"] == 1

        assert result == expected_output_data

    def test_process_data_empty_input(self):
        empty_data = {"roles": [], "reviews": [], "users": []}
        result = format_data(empty_data)

        assert result["companies"] == {}
