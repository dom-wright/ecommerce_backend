from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
from ..db.database import database

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Order not found"}}
)


# defining the order schema we want to receive.
class OrderRequest(BaseModel):
    product_id: int
    customer_id: int
    order_price: float
    quantity: int
    total_price: float
    order_date: datetime
    ship_date: date


# defining the order schema we shall return.
class OrderResponse(BaseModel):
    id: int
    product_id: int
    customer_id: int
    order_price: float
    quantity: int
    total_price: float
    order_date: datetime
    ship_date: date


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[OrderResponse], summary="Get orders.", description="Returns a list of orders.", response_description="The list of orders.",)
async def get_orders(skip: int = 0, limit: int = 10):
    return None


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=OrderResponse, summary="Gets a order.", description="Gets a order based on its ID.", response_description="The order.")
async def get_order(id: int):
    return None


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=OrderResponse, summary="Creates a order", response_description="The created order.")
async def create_order(order: OrderRequest):
    return None


@router.put("/{id}/update", status_code=status.HTTP_200_OK, response_model=OrderResponse, summary="Updates a order.", response_description="The updated order.")
async def update_order(id: int, order: OrderRequest):
    return None


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT, summary="Deletes a order from catelog", description="Finds and deletes a order based on its ID.")
async def delete_order(id: int):
    return None
