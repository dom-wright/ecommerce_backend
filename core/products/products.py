from typing import Mapping
from sqlalchemy import (
    insert,
    update,
    delete
)
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException
)
from ..db.database import (
    database,
    products_table as pt
)
from .schemas import (
    ProductRequest,
    ProductResponse
)
from .dependencies import product_by_id, product_filter

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Product not found"}}
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ProductResponse], summary="Get products.", description="Returns a list of products. The products can be filtered and sorted as desired.", response_description="The list of products.")
async def get_products(product: Mapping = Depends(product_filter)):
    '''
    Parameters:
    product_category (optional) - allows for filtering by product category.
    order_by - records can be ordered by column. defaults to product id.
    order - ascending or descending. defaults to True (ascending).
    limit - limits the number of records returned. defaults to 10.
    skip - skips n number of records that would otherwise be returned. allows for pagination.
    '''
    return product


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ProductResponse, summary="Gets a product.", description="Gets a product based on its ID.", response_description="The product.")
async def get_product_by_id(product: int = Depends(product_by_id)):
    return product


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProductResponse, summary="Creates a product", response_description="The created product.")
async def create_product(product: ProductRequest):
    product_items = product.dict()
    query = insert(pt).values(product_items).returning('*')
    new_product = await database.fetch_one(query)
    if not new_product:
        raise HTTPException(
            status_code=404, detail="Insertion failed.")
    return new_product._mapping


@router.put("/{id}/update", status_code=status.HTTP_200_OK, response_model=ProductResponse, summary="Updates a product.", response_description="The updated product.")
async def update_product(new_product: ProductRequest, product: int = Depends(product_by_id)):
    values = new_product.dict()
    update_query = update(pt).where(pt.c.id == product.id).values(
        **values).returning("*")
    amended_product = await database.fetch_one(update_query)
    return amended_product._mapping


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(product_by_id)], summary="Deletes a product from catelog", description="Finds and deletes a product based on its ID.")
async def delete_product(id: int):
    delete_query = delete(pt).where(pt.c.id ==
                                    id).returning('*')
    deleted_id = await database.execute(delete_query)
    print(f"Product with ID = {deleted_id} Deleted")
    return
