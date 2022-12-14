from pathlib import Path
from datetime import datetime, timedelta
import random
from faker import Faker
from fastapi import HTTPException
from sqlalchemy import select, insert
from ..auth.utils import get_password_hash
from .database import (
    database,
    users_table,
    products_table,
    orders_table,
    order_items_table
)

counties = [
    'Greater London', 'Strathclyde', 'West Lothian', 'North Yorkshire', 'Surrey',
    'Kent', 'Essex', 'Lancashire', 'Durham', 'Glamorgan', 'Cornwall', 'Anglesey', 'Highlands'
]

days = [1, 2, 3, 4, 5, 6, 7]

fake = Faker(locale='en_GB')


async def add_user(n):
    for _ in range(n):
        user_values = _generate_user()
        query = insert(users_table).values(**user_values)
        try:
            await database.execute(query)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=str(e)
            )


def _generate_user():
    first_name = fake.first_name()
    last_name = fake.last_name()
    full_name = f'{first_name} {last_name}'
    username = f'{first_name}_{last_name}'.lower()
    email = f'{first_name}.{last_name}@{fake.domain_name()}'.lower()
    password = 'password'
    hashed_password = get_password_hash(password)
    raw_address = fake.address()
    address = raw_address.replace('\n', ', ').rsplit(', ', 1)[0]
    county = random.choices(counties, weights=(
        30, 10, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5))[0]
    user = {'username': username, 'hashed_password': hashed_password, 'full_name': full_name,
            'email': email, 'address': address, 'county': county}
    return user


async def add_products(n):
    '''
    Ensure csv file is in the same directory as this file.
    Clear products in database before calling this function.
    '''
    if await database.fetch_one(products_table.select()):
        raise HTTPException(
            status_code=400, detail="Data insertion unsuccessful. Products table already contains products. Clear the table first and rerun import.")
    cwd = Path(__file__).parent
    query = f"""COPY products (product_name, product_category, price) FROM '{cwd}/products.csv' DELIMITER ',' CSV HEADER"""
    try:
        await database.execute(query)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(e)
        )


async def add_order(n):
    user_ids = await _get_table_ids(users_table)
    product_ids = await _get_table_ids(products_table)
    for _ in range(n):
        user_id = random.choice(user_ids)
        order_date, ship_date = _generate_order_dates()
        order_status = None
        if ship_date:
            order_status = 'Delivered'
        query = insert(orders_table).values(
            user_id=user_id, order_date=order_date, ship_date=ship_date, order_status=order_status).returning('*')
        try:
            order_id = await database.execute(query)
            await _add_order_items(order_id, product_ids)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=str(e)
            )


async def _add_order_items(order_id, product_ids):
    for _ in range(1, random.randint(2, 4)):
        product_id = random.choice(product_ids)
        quantity = random.choices([1, 2, 3, 4], weights=[60, 25, 10, 5])[0]
        insert_query = insert(order_items_table).values(
            order_id=order_id, product_id=product_id, quantity=quantity)
        try:
            await database.execute(insert_query)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=str(e)
            )


def _generate_order_dates():
    random_time_delta = timedelta(days=random.randrange(0, 180), hours=random.randrange(
        0, 24), minutes=random.randrange(0, 60), seconds=random.randrange(0, 60))
    order_date = datetime.now() - random_time_delta
    days_to_delivery = timedelta(days=random.choices(
        days, weights=[15, 25, 20, 15, 10, 10, 5])[0])
    if days_to_delivery > random_time_delta:
        ship_date = None
    else:
        ship_datetime = order_date + days_to_delivery
        ship_date = ship_datetime.date()
    return order_date, ship_date


async def _get_table_ids(table):
    query = select(table.c.id)
    rows = await database.fetch_all(query)
    ids = [row.id for row in rows]
    return ids
