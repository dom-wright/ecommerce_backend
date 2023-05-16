from enum import Enum


class TablesModel(str, Enum):
    user = "user"
    product = "product"
    order = "order"
