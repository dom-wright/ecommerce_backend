from sqlalchemy import delete
from fastapi import (
    APIRouter,
    Depends,
    status,
    Body
)
from ..db.database import database, products_table as pt
from .schemas import ProductRequest, ProductResponse
from ..dependencies import create_record, update_record
from .dependencies import product_by_id, product_filter

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Product not found"}}
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ProductResponse], summary="Get products.", description="Returns a list of products. The products can be filtered and sorted as desired.", response_description="The list of products.")
async def products(product: product_filter = Depends()):
    return product


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ProductResponse, summary="Gets a product.", description="Gets a product based on its ID.", response_description="The product.")
async def product_by_id(product: product_by_id = Depends()):
    return product


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProductResponse, summary="Creates a product", response_description="The created product.")
async def create_product(product: ProductRequest):
    new_product = await create_record(pt, product)
    return new_product


@router.put("/{id}/update", status_code=status.HTTP_200_OK, response_model=ProductResponse, summary="Updates a product.", response_description="The updated product.")
async def update_product(
    new_values: dict = Body(
        default={}, example='{"product_name": "Trousers", "product_category": "Clothing", "price": 39.99}'),
    product: product_by_id = Depends()
):
    amended_product = await update_record(pt, product, new_values)
    return amended_product


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(product_by_id)], summary="Deletes a product from catelog", description="Finds and deletes a product based on its ID.")
async def delete_product(id: int):
    delete_query = delete(pt).where(pt.c.id ==
                                    id).returning('*')
    deleted_id = await database.execute(delete_query)
    print(f"Product with ID = {deleted_id} Deleted")
    return
