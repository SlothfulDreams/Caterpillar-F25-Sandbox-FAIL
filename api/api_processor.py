from type_annotations.type_dicts import (
    InputData,
    OutputData,
    UserReview,
    RoleData,
    Role,
)

from api.callbacks import (
    role_data_cb,
    sort_reviews,
    calculate_statistics,
)

from typing import Optional


def initialize_schema(roles: list[Role]) -> OutputData:
    """
    Creates a skeleton summary of the json summary we want

    Args:
        roles: list of roles from the json data

    Return:
        Skeleton data of the json summary we want includes all positions
        (Has empty reviews, and empty averages)
    """
    summary: OutputData = {"companies": {}}

    for role in roles:
        company = role["company"]
        role_name = role["role"]
        role_id = role["roleId"]

        if company not in summary["companies"]:
            # Initialize company with no roles/positions
            summary["companies"][role["company"]] = {}

        role_data: RoleData = {
            "name": role_name,
            "id": role_id,
            "avgPay": 0.00,
            "avgRating": 0.00,
            "reviews": [],
        }

        summary["companies"][company][role_name] = role_data

    return summary


def map_user_ids_to_names(input_data: InputData) -> dict[int, str]:
    """
    Maps the userId directly to the name of the person

    Args:
        input_data: The inputted data from the API

    Returns
        A hashmap of user_id being mapped to the person's name
    """
    user_list = input_data["users"]

    user_id_to_name_map = {}

    for user in user_list:
        user_id = user["userId"]
        name = user["name"]
        user_id_to_name_map[user_id] = name

    return user_id_to_name_map


def find_role_location(schema: OutputData, role_id: int) -> Optional[RoleData]:
    """
    Finds the specific role location in the schema using the ID

    Args:
        schema: The output data structure
        role_id: The role ID to find

    Returns:
        The role data container if found, None otherwise
    """
    for _, roles in schema["companies"].items():
        for _, role_data in roles.items():
            if role_data["id"] == role_id:
                return role_data
    return None


def add_reviews_to_roles(schema: OutputData, input_data: InputData):
    """
    Add reviews to each role position

    Args:
        schema: The output of what the data should look like
        input_data: The data received from the API
    """
    reviews = input_data["reviews"]
    user_id_to_name = map_user_ids_to_names(input_data)

    for review in reviews:
        roleId = review["roleId"]
        role_schema_location = find_role_location(schema, roleId)

        user_id = review["userId"]
        overall_score = review["overallScore"]
        hourly_pay = review["hourlyPay"]
        ratingId = review["ratingId"]

        user_review: UserReview = {
            "user": user_id_to_name[user_id],
            "rating": overall_score,
            "pay": hourly_pay,
            "review": ratingId,
        }

        if role_schema_location:
            role_schema_location["reviews"].append(user_review)


def format_data(input_data: InputData) -> OutputData:
    """
    Reformat the JSON data into the intended format

    Args:
        input_data: The inputted data from the API

    Returns:
        OutputData: The intended structure of the reformatted JSON
    """
    # Step 1: Create the skeleton structure of the output data
    final_schema = initialize_schema(input_data["roles"])

    # Step 2: Start filling in the reviews for each position
    add_reviews_to_roles(final_schema, input_data)

    # Step 3: Sort the reviews in descending order
    role_data_cb(final_schema, sort_reviews)

    # Step 4: Calculate the averages for pay and rating
    role_data_cb(final_schema, calculate_statistics)

    return final_schema
