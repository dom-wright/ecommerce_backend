from enum import Enum


class OrderStatusModel(str, Enum):
    pending = "Pending"
    accepted = "Accepted"
    delivered = "Delivered"
    dispatched = "Dispatched"
    cancelled = "Cancelled"


class OrderColsModel(str, Enum):
    id = "id"
    customer_id = "customer_id"
    order_date = "order_date"
    order_status = "order_status"
    ship_date = "ship_date"
