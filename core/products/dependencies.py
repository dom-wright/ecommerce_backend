from fastapi import HTTPException
from sqlalchemy import (
    select,
    text
)
from ..db.database import (
    database,
    products_table as pt
)
from .schemas import (
    ProductCategoriesModel,
    ProductColsModel
)
from ..enums import ColumnOrderModel


async def product_by_id(id: int):
    query = select(pt).where(pt.c.id == id)
    record = await database.fetch_one(query)
    if not record:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID = {id} not found.")
    return record


async def product_filter(product_category: ProductCategoriesModel | None = None, order_by: ProductColsModel = ProductColsModel.id, order: ColumnOrderModel = ColumnOrderModel.ASC, limit: int = 10, skip: int = 0):
    query = select(pt)
    if product_category:
        query = query.where(pt.c.product_category == product_category)
    query = query.order_by(
        text(f'{order_by} {order.name}')).limit(limit).offset(skip)
    results = await database.fetch_all(query)
    return results
