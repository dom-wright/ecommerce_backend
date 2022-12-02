from uuid import UUID
from enum import Enum
from pydantic import BaseModel, Field


# product request schema
class ProductRequest(BaseModel):
    product_name: str = Field(min_length=1, max_length=100)
    product_category: str = Field(min_length=1, max_length=100)
    price: float

    class Config:
        schema_extra = {
            "example": {
                "product_name": "FooBar",
                "product_category": "Headwear",
                "price": 35.99
            }
        }


# product response schema
class ProductResponse(BaseModel):
    id: int
    product_sku: UUID
    product_name: str
    product_category: str
    price: str

    class Config:
        schema_extra = {
            "example": {
                "id": "12",
                "product_sku": "4e7dd739-f000-4840-9740-b427c52d5c69",
                "product_name": "Dress",
                "product_category": "Clothing",
                "price": 119.99
            }
        }


'''enum models'''


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
