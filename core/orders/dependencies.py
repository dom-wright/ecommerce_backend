from fastapi import HTTPException, Query, Depends
from sqlalchemy import (
    select,
    text,
    insert
)
from ..db.database import (
    database,
    users_table as ut,
    orders_table as ot,
    order_items_table as oi,
    products_table as pt
)
from .schemas import (
    OrderItemsRequest,
    OrderResponse,
    OrderItemsResponse
)
from .enums import OrderColsModel, OrderStatusModel
from ..auth.dependencies import get_user_by_id
from ..products.dependencies import product_by_id
from ..enums import ColumnOrderModel


'''GET'''


async def get_orders(status: OrderStatusModel | None = None, county: str | None = Query(default=None, title="Filter by region.", description="Choose a region (County) of the UK e.g. 'Cornwall', 'West Lothian'."), order_by: OrderColsModel = OrderColsModel.order_date, order: ColumnOrderModel = ColumnOrderModel.DESC, limit: int = 10, skip: int = 0):
    query = select(ot).join_from(ot, ut)
    if status:
        query = query.where(ot.c.order_status == status)
    if county:
        query = query.where(ut.c.county == county)
    query = query.order_by(
        text(f'{order_by} {order.name}')).limit(limit).offset(skip)
    orders = await database.fetch_all(query)
    return orders


async def get_orders_by_user(id: int):
    query = select(ot).where(ot.c.user_id == id)
    orders = await database.fetch_all(query)
    if not orders:
        raise HTTPException(
            status_code=404, detail=f"Orders for user with ID = {id} not found."
        )
    return orders


async def get_order_by_id(order_id: int):
    query = select(ot).where(ot.c.id == order_id)
    order = await database.fetch_one(query)
    if not order:
        raise HTTPException(
            status_code=404, detail=f"Order with ID = {id} not found."
        )
    return order


async def get_order_by_id_with_items(order_id: int, with_items: bool = False):
    order = await get_order_by_id(order_id)
    if with_items:
        order = await _get_order_with_items(order)
    return order


async def _get_order_with_items(order: OrderResponse):
    user = await get_user_by_id(order['user_id'])
    order_items_query = select(oi).where(oi.c.order_id == order["id"])
    order_items = await database.fetch_all(order_items_query)
    order_items_with_products = await _get_items_with_product(order_items)
    full_order = {
        "user": user,
        "order": order,
        "order_items": order_items_with_products
    }
    return full_order


async def _get_items_with_product(order_items: list[OrderItemsResponse]):
    items_with_products = []
    for item in order_items:
        item_dict = dict(item)
        product = await product_by_id(item_dict["product_id"])
        item_dict.update({"product": dict(product)})
        items_with_products.append(item_dict)
    return items_with_products


'''CREATE / UPDATE'''


async def create_new_order(user_id: int, orderItems: list[OrderItemsRequest]):
    insert_order_query = insert(ot).values(
        user_id=user_id).returning('*')
    order = await database.fetch_one(insert_order_query)
    if not order:
        raise HTTPException(
            status_code=404, detail=f"Order with ID = {id} not found.")
    await _create_new_order_items(order, orderItems)
    return order


async def _create_new_order_items(order: OrderResponse, orderItems: list[OrderItemsRequest]):
    insert_order_items_query = insert(oi).returning('*')
    order_items = [{**orderItem.dict(), "order_id": order.id}
                   for orderItem in orderItems]
    await database.execute_many(insert_order_items_query, order_items)
