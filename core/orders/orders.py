from typing import Mapping
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException
)
from sqlalchemy import delete
from ..db.database import database, orders_table as ot
from .schemas import (
    OrderRequest,
    OrderItemsRequest,
    OrderResponse,
    OrderWithItemsResponse,
    OrdersByCustomerResponse
)
from ..customers.dependencies import customer_by_id
from ..dependencies import update_record
from .dependencies import (
    get_orders,
    get_order_by_id,
    get_order_by_id_with_items,
    create_new_order,
    get_orders_by_customer
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Order not found"}}
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrderResponse], summary="Get orders.", description="Returns a list of orders.", response_description="The list of orders.",)
async def orders(orders: list[OrderResponse] = Depends(get_orders)):
    return orders


@router.get("/customer/{id}", status_code=status.HTTP_200_OK, response_model=OrdersByCustomerResponse, summary="Get orders.", description="Returns a list of orders.", response_description="The list of orders.",)
async def orders_by_customer(id: int, orders: list[OrdersByCustomerResponse] = Depends(get_orders_by_customer)):
    customer = await customer_by_id(id)
    return {"customer": customer, "orders": orders}


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=OrderWithItemsResponse | OrderResponse, summary="Gets a order based on its ID.", description="Gets the order using the order ID. Option to include full details, including customer, items & products.", response_description="The order.")
async def order_by_id(order: Mapping = Depends(get_order_by_id_with_items)):
    return order


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=OrderWithItemsResponse, summary="Creates a new order", response_description="The created order.")
async def create_order(customer_id: int, orderItems: list[OrderItemsRequest]):
    new_order = await create_new_order(customer_id, orderItems)
    full_order = await get_order_by_id_with_items(new_order.id, with_items=True)
    return full_order


@router.put("/{id}/update", status_code=status.HTTP_200_OK, response_model=OrderResponse, summary="Updates a order.", response_description="The updated order.")
async def update_product(new_values: OrderRequest, order: int = Depends(get_order_by_id)):
    new_values_dict = new_values.dict()
    amended_order = await update_record(ot, order, new_values_dict)
    return amended_order


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT, summary="Deletes a order from catelog", description="Finds and deletes a order based on its ID.")
async def delete_order(id: int):
    delete_query = delete(ot).where(ot.c.id == id).returning('*')
    deleted_id = await database.execute(delete_query)
    if not deleted_id:
        raise HTTPException(
            status_code=404, detail=f"Deletion failed. Order with ID = {id} not found.")
    return f"Order with ID = {deleted_id} Deleted"
