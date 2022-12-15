import os

# you can use the command 'openssl rand -hex 32' in the terminal to create a random secret key.
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# middleware
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://localhost"
]


# application metadata

tags_metadata = [
    {
        "name": "Home"
    },
    {
        "name": "Auth",
        "description": "Operations regarding login and authentication."
    },
    {
        "name": "Orders",
        "description": "Operations with orders",
    },
    {
        "name": "Products",
        "description": "Operations with products.",
    },
    {
        "name": "Users",
        "description": "Operations with users.",
    },
    {
        "name": "Admin",
        "description": "Administrative operations. Add data to the application here.",
    }
]


site_description = """
## Summary
Welcome to my ecommerce application.
Here you can perform CRUD operations on three main subjects.

#### Users
A list of customers, staff members and superusers, all with varying access to endpoints / resources.

#### Products
A list of the products this company sells.

#### Orders
A list of orders and their current status.
"""
