import os
import sys

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


# logging configurations
FASTAPI_LOG_LEVEL = 'INFO'

logging_config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%d-%b-%y %H:%M:%S'
        },
        'verbose': {
            'format': '%(asctime)s - module: %(module)s - function:%(funcName)s - line:%(lineno)d - level:%(levelname)s - message:%(message)s',
            'datefmt': '%d-%b-%y %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': FASTAPI_LOG_LEVEL,
            'formatter': 'simple',
            'stream': sys.stdout
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'WARNING',
            'formatter': 'verbose',
            'filename': 'orders_app.log'
        }
    },
    'loggers': {
        'orderLogger': {
            'handlers': ['file'],
            'propagate': True
        }
    },
    'root': {
        'handlers': ['console'],
        'level': FASTAPI_LOG_LEVEL
    }
}


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
