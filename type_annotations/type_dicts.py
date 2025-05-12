from typing import Dict, List, TypedDict


class Role(TypedDict):
    role: str
    roleId: int
    company: str


class Review(TypedDict):
    roleId: int
    ratingId: int
    overallScore: int
    hourlyPay: int
    userId: int


class User(TypedDict):
    name: str
    userId: int
    reviews: List[int]


class InputData(TypedDict):
    roles: List[Role]
    reviews: List[Review]
    users: List[User]


class UserReview(TypedDict):
    user: str
    rating: int
    pay: int
    review: int


class RoleData(TypedDict):
    name: str
    id: int
    avgPay: float
    avgRating: float
    reviews: List[UserReview]


# Do not know the exact role name
CompanyRoles = Dict[str, RoleData]


class OutputData(TypedDict):
    companies: Dict[str, CompanyRoles]
