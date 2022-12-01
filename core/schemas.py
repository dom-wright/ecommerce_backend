from datetime import datetime, date
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


'''
pydantic request / response models

see https://fastapi.tiangolo.com/tutorial/body-nested-models/#__tabbed_3_3 for nested pydantic models.
 
'''


# customer request schema
class CustomerRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    address: str = Field(min_length=1, max_length=100)
    county: str = Field(min_length=1, max_length=100)
    email: EmailStr


# customer response schema
class CustomerResponse(BaseModel):
    id: int
    name: str
    address: str
    county: str
    email: EmailStr


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


class OrderItemsRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderRequest(BaseModel):
    customer_id: int
    orderItems: list[OrderItemsRequest]


class OrderItemsResponse(BaseModel):
    product: ProductResponse
    product_unit_price: float
    quantity: int


class OrderResponse(BaseModel):
    id: int
    customer: CustomerResponse
    order_date: datetime
    ship_date: date
    orderItems: OrderItemsResponse


'''enum models'''


class ColumnOrderModel(str, Enum):
    ASC = 'ascending'
    DESC = 'descending'


class CustomerModel(str, Enum):
    id = 'id'
    name = "name"
    address = "address"
    county = "county"
    email = "email"


class ProductColsModel(str, Enum):
    id = 'id'
    product_name = "product_name"
    product_category = "product_category"
    price = "price"


class CategoriesModel(str, Enum):
    clothing = "Clothing"
    footwear = "Footwear"
    headwear = "Headwear"
    accessories = "Accessories"
