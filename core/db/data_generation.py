from pathlib import Path
from datetime import datetime, timedelta
import random
from faker import Faker
from fastapi import HTTPException
from sqlalchemy import select, insert
from .database import (
    database,
    customers_table,
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


async def add_customer(n):
    for _ in range(n):
        name, address, county, email = _generate_customer()
        query = insert(customers_table).values(
            name=name, address=address, county=county, email=email)
        try:
            await database.execute(query)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=str(e))


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
            status_code=500, detail=str(e))


async def add_order(n):
    customer_ids = await _get_customer_ids()
    product_ids = await _get_product_ids()
    for _ in range(n):
        customer_id = random.choice(customer_ids)
        order_date, ship_date = _generate_order_dates()
        query = insert(orders_table).values(
            customer_id=customer_id, order_date=order_date, ship_date=ship_date).returning('*')
        try:
            order_id = await database.execute(query)
            await add_order_items(order_id, product_ids)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=str(e))


async def add_order_items(order_id, product_ids):
    for _ in range(1, random.randint(2, 4)):
        product_id = random.choice(product_ids)
        quantity = random.choices([1, 2, 3, 4], weights=[60, 25, 10, 5])[0]
        insert_query = insert(order_items_table).values(
            order_id=order_id, product_id=product_id, quantity=quantity)
        try:
            await database.execute(insert_query)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=str(e))


async def _get_customer_ids():
    customer_query = select(customers_table.c.id)
    customer_results = await database.fetch_all(customer_query)
    customer_ids = [row[0] for row in customer_results]
    return customer_ids


async def _get_product_ids():
    product_query = select(products_table.c.id)
    product_results = await database.fetch_all(product_query)
    product_ids = [row[0] for row in product_results]
    return product_ids


def _generate_customer():
    first_name = fake.first_name()
    last_name = fake.last_name()
    name = f'{first_name} {last_name}'
    raw_address = fake.address()
    address = raw_address.replace('\n', ', ').rsplit(', ', 1)[0]
    county = random.choices(counties, weights=(
        30, 10, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5))[0]
    email = f'{first_name}.{last_name}@{fake.domain_name()}'
    return name, address, county, email


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
