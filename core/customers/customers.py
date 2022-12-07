from fastapi import APIRouter, status, HTTPException
from ..db.database import database
from .schemas import (
    CustomerRequest,
    CustomerResponse
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    responses={404: {"description": "Customer not found"}}
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CustomerResponse], summary="Get customers", description="Returns a list of customers", response_description="The list of customers.",)
async def get_customers(skip: int = 0, limit: int = 10):
    select_query = f"""SELECT * FROM customers OFFSET :skip LIMIT :limit;"""
    customers = await database.fetch_all(select_query, {'skip': skip, 'limit': limit})
    return customers


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CustomerResponse, summary="Gets a customer", description="Gets a customer based on their ID.", response_description="The customer.")
async def get_customer(id: int):
    query = """SELECT * FROM customers WHERE id = :id;"""
    customer = await database.fetch_one(query, {'id': id})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=CustomerResponse, summary="Creates a customer", response_description="The created customer.")
async def create_customer(customer: CustomerRequest):
    customer = customer.dict()
    create_query = """INSERT INTO customers(name, address, county, email) VALUES (:name, :address, :county, :email);"""
    await database.execute(create_query, customer)
    select_query = "SELECT * FROM customers WHERE email = :email"
    new_customer = await database.fetch_one(select_query, values={"email": customer["email"]})
    if not new_customer:
        raise HTTPException(
            status_code=404, detail="Customer creation failed.")
    return new_customer


@router.put("/{id}/update", status_code=status.HTTP_200_OK, summary="Updates a customer", response_description="The updated customer.")
async def update_customer(id: int, customer: CustomerRequest):
    customer = customer.dict()
    customer['id'] = id
    update_query = """UPDATE customers SET name = :name, address = :address, county = :county, email = :email WHERE id = :id"""
    await database.execute(update_query, customer)
    select_query = "SELECT * FROM customers WHERE id = :id"
    amended_customer = await database.fetch_one(select_query, values={"id": id})
    if not amended_customer:
        raise HTTPException(
            status_code=404, detail="Customer not found. Could not update.")
    return amended_customer


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT, summary="Deletes a customer", description="Finds and deletes a customer based on their ID.")
async def delete_customer(id: int):
    select_query = "SELECT * FROM customers WHERE id = :id"
    customer = await database.fetch_one(select_query, values={"id": id})
    if not customer:
        raise HTTPException(
            status_code=400, detail="Deletion failed. Customer not found.")
    delete_query = """DELETE FROM customers WHERE id = :id RETURNING *"""
    deleted_id = await database.execute(delete_query, values={"id": id})
    print(f"Customer with ID = {deleted_id} deleted")
    return
