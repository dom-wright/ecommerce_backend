from enum import Enum
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Union
from uuid import UUID
from ..db.database import (
    database,
    products_table as pt
)
from sqlalchemy import (
    text,
    select,
    insert,
    update,
    delete
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Product not found"}}
)


# defining the product schema we want to receive.
class ProductRequest(BaseModel):
    product_name: str
    product_category: str
    price: float


# defining the product schema we shall return.
class ProductResponse(BaseModel):
    id: int
    product_sku: UUID
    product_name: str
    product_category: str
    price: str


class CategoriesModel(str, Enum):
    clothing = "clothing"
    footwear = "footwear"
    headwear = "headwear"
    accessories = "accessories"


class ProductColsModel(str, Enum):
    id = 'id'
    product_name = "product_name"
    product_category = "product_category"
    price = "price"


class ProductOrderModel(str, Enum):
    ascending = 'Asc'
    descending = 'Desc'


def product_filter(product_category, order_by, order, limit, skip):
    query = select(pt)
    if product_category:
        query = query.where(pt.c.product_category == product_category)
    query = query.order_by(
        text(f'{order_by} {order}')).limit(limit).offset(skip)
    return query


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProductResponse], summary="Get products.", description="Returns a list of products. The products can be filtered and sorted as desired.", response_description="The list of products.")
async def get_products(product_category: Union[CategoriesModel, None] = None, order_by: ProductColsModel = ProductColsModel.id, order: ProductOrderModel = ProductOrderModel.ascending, limit: int = 10, skip: int = 0):
    '''
    Parameters:
    product_category (optional) - allows for filtering by product category.
    order_by - records can be ordered by column. defaults to product id.
    order - ascending or descending. defaults to True (ascending).
    limit - limits the number of records returned. defaults to 10.
    skip - skips n number of records that would otherwise be returned. allows for pagination.
    '''
    query = product_filter(product_category, order_by, order, limit, skip)
    results = await database.fetch_all(query)
    return results


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ProductResponse, summary="Gets a product.", description="Gets a product based on its ID.", response_description="The product.")
async def get_product(id: int):
    select_query = select(pt).where(pt.c.id == id)
    result = await database.fetch_one(select_query)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID = {id} not found.")
    return result


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProductResponse, summary="Creates a product", response_description="The created product.")
async def create_product(product: ProductRequest):
    product_items = product.dict()
    query = insert(pt).values(product_items).returning('*')
    result_id = await database.execute(query)
    if not result_id:
        raise HTTPException(
            status_code=404, detail="Insertion failed.")
    query = select(pt).where(
        pt.c.id == result_id)
    new_product = await database.fetch_one(query)
    return new_product


@router.put("/{id}/update", status_code=status.HTTP_200_OK, response_model=ProductResponse, summary="Updates a product.", response_description="The updated product.")
async def update_product(id: int, product_fields: dict):
    update_query = update(pt).where(pt.c.id ==
                                    id).values(product_fields).returning("*")
    result_id = await database.execute(update_query)
    if not result_id:
        raise HTTPException(
            status_code=404, detail=f"Update failed. Customer with ID = {id} not found.")
    query = select(pt).where(pt.c.id == result_id)
    amended_product = await database.fetch_one(query)
    return amended_product


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT, summary="Deletes a product from catelog", description="Finds and deletes a product based on its ID.")
async def delete_product(id: int):
    delete_query = delete(pt).where(pt.c.id ==
                                    id).returning('*')
    deleted_id = await database.execute(delete_query)
    if not deleted_id:
        raise HTTPException(
            status_code=404, detail=f"Deletion failed. Customer with ID = {id} not found.")
    return f"Product with ID = {deleted_id} Deleted"
