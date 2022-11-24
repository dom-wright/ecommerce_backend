from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List
from ..database import database

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    responses={404: {"description": "Customer not found"}}
)


# defining the customer schema we want to receive.
class CustomerRequest(BaseModel):
    name: str
    address: str
    city: str
    email: str


# defining the customer schema we shall return.
class CustomerResponse(BaseModel):
    id: int
    name: str
    address: str
    city: str
    email: str


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CustomerResponse], summary="Get customers", description="Returns a list of customers", response_description="The list of customers.",)
async def get_customers(skip: int = 0, limit: int = 10):
    query = """SELECT * FROM customers ORDER BY name OFFSET :skip LIMIT :limit;"""
    rows = await database.fetch_all(query, {'skip': skip, 'limit': limit})
    return rows


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CustomerResponse, summary="Gets a customer", description="Gets a customer based on their ID.", response_description="The customer.")
async def get_customer(id: int):
    query = """SELECT * FROM customers WHERE id = :id;"""
    customer = await database.fetch_one(query, {'id': id})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer


@router.post("/create", status_code=status.HTTP_201_CREATED, summary="Creates a customer", response_description="The created customer.")
async def create_customer(customer: CustomerRequest):
    customer = customer.dict()
    create_query = """INSERT INTO customers(name, address, city, email) VALUES (:name, :address, :city, :email);"""
    await database.execute(create_query, customer)
    select_query = "SELECT * FROM customers WHERE email = :email"
    result = await database.fetch_one(select_query, values={"email": customer["email"]})
    if not result:
        raise HTTPException(
            status_code=404, detail="Customer creation failed.")
    return result


@router.put("/{id}/update", status_code=status.HTTP_200_OK, summary="Updates a customer", response_description="The updated customer.")
async def update_customer(id: int, customer: CustomerRequest):
    customer = customer.dict()
    customer['id'] = id
    update_query = """UPDATE customers SET name = :name, address = :address, city = :city, email = :email WHERE id = :id"""
    await database.execute(update_query, customer)
    select_query = "SELECT * FROM customers WHERE id = :id"
    result = await database.fetch_one(select_query, values={"id": id})
    if not result:
        raise HTTPException(
            status_code=404, detail="Customer not found. Could not update.")
    return result


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT, summary="Deletes a customer", description="Finds and deletes a customer based on their ID.")
async def delete_customer(id: int):
    select_query = "SELECT * FROM customers WHERE id = :id"
    customer = await database.fetch_one(select_query, values={"id": id})
    if not customer:
        raise HTTPException(
            status_code=400, detail="Deletion failed. Customer not found.")
    delete_query = """DELETE FROM customers WHERE id = :id"""
    await database.execute(delete_query, values={"id": id})
    return "Customer Deleted"
