from enum import Enum
from fastapi import APIRouter, status
from ..db.database import (
    add_customer,
    add_products,
    add_order
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


class TablesModel(str, Enum):
    customer = "customer"
    product = "product"
    order = "order"


@router.post("/create/", status_code=status.HTTP_201_CREATED, response_model=str, summary="Create new records.", description="Create new records for the tables.")
async def get_products(table: TablesModel, num: int = 0):
    insertion_functions = {
        TablesModel.customer: add_customer,
        TablesModel.product: add_products,
        TablesModel.order: add_order
    }
    await insertion_functions[table](num)
    return f'{num} insertions made.'
