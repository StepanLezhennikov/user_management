from enum import Enum


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class SortBy(str, Enum):
    created_at = "created_at"
    first_name = "first_name"
    last_name = "last_name"
