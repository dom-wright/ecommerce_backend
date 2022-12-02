from enum import Enum
from pydantic import BaseModel, EmailStr, Field


# customer request schema
class CustomerRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    address: str = Field(min_length=1, max_length=100)
    county: str = Field(min_length=1, max_length=100)
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "address": "123 Fake Street",
                "city": "Faketown",
                "email": "jane.doe@example.com"
            }
        }


# customer response schema
class CustomerResponse(BaseModel):
    id: int
    name: str
    address: str
    county: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "id": 34,
                "name": "Jane Doe",
                "address": "123 Fake Street",
                "city": "Faketown",
                "email": "jane.doe@example.com"
            }
        }


'''enum models'''


class CustomerModel(str, Enum):
    id = 'id'
    name = "name"
    address = "address"
    county = "county"
    email = "email"


class TablesModel(str, Enum):
    customer = "customer"
    product = "product"
    order = "order"
