from enum import Enum


class TablesModel(str, Enum):
    user = "Users"
    product = "Products"
    order = "Orders"
