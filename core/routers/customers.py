from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    responses={404: {"description": "Not found"}}
)


# defining the customer schema we want to receive.
class CustomerRequest(BaseModel):
    name: str
    address: str
    email: str


# defining the customer schema we shall return.
class CustomerResponse(BaseModel):
    id: str
    name: str
    address: str
    email: str


customers_list = [
    {
        "id": "1",
        "name": "Jane Doe",
        "address": "123 Fake Street, Faketown",
        "email": "jane.doe@example.com"
    },
    {
        "id": "2",
        "name": "Jose Doe",
        "address": "321 Calle Falsa, Ciudad de Fako",
        "email": "jose.doe@ejemplo.com"
    }
]


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CustomerResponse], summary="Get customers", description="Returns a list of customers", response_description="The list of customers.",)
async def get_customers(skip: int = 0, limit: int = 10):
    '''
    logic to return customers from database
    '''
    return customers_list


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CustomerResponse, summary="Gets a customer", description="Gets a customer based on their ID.", response_description="The customer.")
async def get_customer(id: str):
    '''
    logic to find customer in database
    '''
    customer = next(
        (customer for customer in customers_list if customer["id"] == id), None)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer


@router.post("/create", status_code=status.HTTP_201_CREATED, summary="Creates a customer", response_description="The created customer.")
async def create_customer(customer: CustomerRequest):
    """
    creates a customer using the following information:

    - **name**: required - each customer must have a name
    - **address**: required - each customer must have an address to deliver to
    - **email**: required - each customer must have a unique email.
    """
    customer = customer.dict()
    id = int(customers_list[-1]["id"])
    customer["id"] = str(id + 1)
    customers_list.append(customer)
    return customer


@router.put("/{id}/update", status_code=status.HTTP_200_OK, summary="Updates a customer", response_description="The updated customer.")
async def update_customer(id: str, customer_changes: dict):
    '''
    logic to update a customer in the database.
    '''
    for customer in customers_list:
        if customer["id"] == id:
            customer.update(customer_changes)
            return customer
    raise HTTPException(status_code=400, detail="Customer not found.")


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT, summary="Deletes a customer", description="Finds and deletes a customer based on their ID.")
async def delete_customer(id: str):
    '''
    logic to find customer record in database and delete it.
    '''
    for customer in customers_list:
        if customer['id'] == id:
            customers_list.remove(customer)
            return None
    raise HTTPException(status_code=400, detail="Customer not found.")
