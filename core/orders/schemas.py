from datetime import datetime, date
from pydantic import BaseModel, validator, Field
from ..customers.schemas import CustomerResponse
from ..products.schemas import ProductResponse
from .enums import OrderStatusModel


class OrderRequest(BaseModel):
    ship_date: date | None = None
    order_status: OrderStatusModel

    @validator('order_status')
    def order_status_permitted(cls, v, values):
        if v == 'Delivered' and not values.get("ship_date"):
            raise ValueError(
                "If the order has been delivered, you must submit the date the order was shipped."
            )
        elif v != 'Delivered' and values.get("ship_date"):
            raise ValueError(
                "You may only submit a ship_date if the order has been delivered."
            )
        return v.title()

    class Config:
        schema_extra = {
            "example": {
                "ship_date": "2022-08-30",
                "order_status": "Delivered"
            }
        }


class OrderItemsRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

    class Config:
        schema_extra = {
            "example": {
                "product_id": 46,
                "quantity": 2
            }
        }


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    order_date: datetime
    ship_date: date | None
    order_status: str

    class Config:
        schema_extra = {
            "example": {
                "id": 12,
                "customer_id": 34,
                "order_date": "2022-08-27 15:43:01.843467",
                "ship_date": "2022-08-30",
                "order_status": "Delivered"
            }
        }


class OrderItemsResponse(BaseModel):
    order_id: int
    product_id: int
    product_unit_price: str
    quantity: int
    product: ProductResponse

    class Config:
        schema_extra = {
            "example": {
                "order_id": 12,
                "product_id": 23,
                "product_unit_price": "$39.99",
                "quantity": 1,
                "product": {
                    "product_id": 11,
                    "product_sku": "71c7d3a5-dd89-4bf7-9088-db901a88cbe7",
                    "product_name": "Coat",
                    "product_category": "Clothing",
                    "price": "$99.99"
                }
            }
        }


class OrderWithItemsResponse(BaseModel):
    customer: CustomerResponse
    order: OrderResponse
    order_items: list[OrderItemsResponse]

    class Config:
        schema_extra = {
            "example": {
                "order": {
                    "id": 12,
                    "customer_id": 34,
                    "order_date": "2022-08-27 15:43:01.843467",
                    "ship_date": "2022-08-30",
                    "order_status": "Delivered"
                },
                "customer": {
                    "id": 34,
                    "name": "Jane Doe",
                    "address": "123 Fake Street",
                    "county": "Fakeshire",
                    "email": "jane.doe@example.com"
                },
                "order_items": [
                    {
                        "order_id": 12,
                        "product_id": 11,
                        "product_unit_price": "$99.99",
                        "quantity": 1,
                        "product": {
                            "product_id": 11,
                            "product_sku": "71c7d3a5-dd89-4bf7-9088-db901a88cbe7",
                            "product_name": "Coat",
                            "product_category": "Clothing",
                            "price": "$99.99"
                        }
                    }, {
                        "order_id": 12,
                        "product_id": 33,
                        "product_unit_price": "$29.99",
                        "quantity": 3,
                        "product": {
                            "id": 33,
                            "product_sku": "64bebdf8-162f-4af3-bf49-42e44f92796e",
                            "product_name": "T-Shirt",
                            "product_category": "Clothing",
                            "price": "$29.99"
                        }
                    }
                ]
            }
        }


class OrdersByCustomerResponse(BaseModel):
    customer: CustomerResponse
    orders: list[OrderResponse]

    class Config:
        schema_extra = {
            "example": {
                "customer": {
                    "id": 34,
                    "name": "Jane Doe",
                    "address": "123 Fake Street",
                    "county": "Fakeshire",
                    "email": "jane.doe@example.com"
                },
                "orders": [
                    {
                        "id": 12,
                        "customer_id": 34,
                        "order_date": "2022-08-27 15:43:01.843467",
                        "ship_date": "2022-08-30",
                        "order_status": "Delivered"
                    },
                    {
                        "id": 17,
                        "customer_id": 34,
                        "order_date": "2022-10-13T17:52:59.895709",
                        "ship_date": "2022-10-16",
                        "order_status": "Pending"
                    }
                ]
            }
        }
