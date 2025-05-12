import pytest
from type_annotations.type_dicts import InputData, OutputData


@pytest.fixture
def input_data() -> InputData:
    return {
        "roles": [
            {"role": "Software Developer", "roleId": 25, "company": "Amazon"},
            {"role": "UX Designer", "roleId": 114, "company": "Apple"},
            {"role": "Site Reliability Engineer", "roleId": 654, "company": "Meta"},
        ],
        "reviews": [
            {
                "roleId": 25,
                "ratingId": 9935,
                "overallScore": 1,
                "hourlyPay": 38,
                "userId": 0,
            },
            {
                "roleId": 114,
                "ratingId": 1520,
                "overallScore": 1,
                "hourlyPay": 22,
                "userId": 1,
            },
            {
                "roleId": 114,
                "ratingId": 4582,
                "overallScore": 2,
                "hourlyPay": 36,
                "userId": 0,
            },
            {
                "roleId": 654,
                "ratingId": 4257,
                "overallScore": 5,
                "hourlyPay": 33,
                "userId": 2,
            },
        ],
        "users": [
            {"name": "Sarah Zhang", "userId": 0, "reviews": [9935, 4582]},
            {"name": "Rishi Kanabar", "userId": 1, "reviews": [1520]},
            {"name": "Christine Cho", "userId": 2, "reviews": [4257]},
        ],
    }


@pytest.fixture
def expected_output_data() -> OutputData:
    return {
        "companies": {
            "Amazon": {
                "Software Developer": {
                    "name": "Software Developer",
                    "id": 25,
                    "avgPay": 38.00,
                    "avgRating": 1.00,
                    "reviews": [
                        {"user": "Sarah Zhang", "rating": 1, "pay": 38, "review": 9935}
                    ],
                }
            },
            "Apple": {
                "UX Designer": {
                    "name": "UX Designer",
                    "id": 114,
                    "avgPay": 29.00,
                    "avgRating": 1.50,
                    "reviews": [
                        {"user": "Sarah Zhang", "rating": 2, "pay": 36, "review": 4582},
                        {
                            "user": "Rishi Kanabar",
                            "rating": 1,
                            "pay": 22,
                            "review": 1520,
                        },
                    ],
                }
            },
            "Meta": {
                "Site Reliability Engineer": {
                    "name": "Site Reliability Engineer",
                    "id": 654,
                    "avgPay": 33.00,
                    "avgRating": 5.00,
                    "reviews": [
                        {
                            "user": "Christine Cho",
                            "rating": 5,
                            "pay": 33,
                            "review": 4257,
                        }
                    ],
                }
            },
        }
    }
