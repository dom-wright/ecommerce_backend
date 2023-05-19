from fastapi import APIRouter, status
from src.db.data_generation import (
    add_user,
    add_products,
    add_order
)
from .enums import TablesModel

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post("/create/", status_code=status.HTTP_201_CREATED, response_model=str, summary="Create new records.", description="Create new records for the tables.")
async def get_products(table: TablesModel, num: int = 0):
    insertion_functions = {
        TablesModel.user: add_user,
        TablesModel.product: add_products,
        TablesModel.order: add_order
    }
    await insertion_functions[table](num)
    return f'Data inserted.'
