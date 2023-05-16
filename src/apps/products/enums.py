from enum import Enum


class ProductColsModel(str, Enum):
    id = 'id'
    product_name = "product_name"
    product_category = "product_category"
    price = "price"


class ProductCategoriesModel(str, Enum):
    clothing = "Clothing"
    footwear = "Footwear"
    headwear = "Headwear"
    accessories = "Accessories"
