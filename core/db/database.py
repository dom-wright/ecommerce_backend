from pathlib import Path
import random
from databases import Database
from sqlalchemy import (
    ForeignKey,
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    DateTime,
    Date,
    Numeric,
    insert,
    select
)
from .data import (
    generate_customer,
    generate_order
)


# DATABASES
DATABASE_URL = 'postgresql+asyncpg://localhost:5432/my_orders_db'
database = Database(DATABASE_URL)

metadata = MetaData()
engine = create_engine(DATABASE_URL)

customers_table = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(length=100)),
    Column("address", String(length=100)),
    Column("county", String(length=100)),
    Column("email", String(length=100))
)

products_table = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("product_sku", String(length=32)),
    Column("product_name", String(length=100)),
    Column("product_category", String(length=100)),
    Column("price", Numeric(precision=10, scale=2))
)

orders_table = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey(
        "customers.id")),
    Column("order_date", DateTime),
    Column("ship_date", Date)
)

order_items = Table(
    "order_items",
    metadata,
    Column("order_id", Integer, ForeignKey(
        "orders.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey(
        "products.id"), primary_key=True),
    Column("product_unit_price", Numeric(precision=10, scale=2)),
    Column("quantity", Integer)
)


async def add_customer(n):
    for _ in range(n):
        name, address, county, email = generate_customer()
        query = insert(customers_table).values(
            name=name, address=address, county=county, email=email)
        try:
            await database.execute(query)
        except Exception as e:
            print(e)


async def add_products(n):
    # ensure csv file is in the same directory as this file.
    cwd = Path(__file__).parent
    query = f"""COPY products (product_name, product_category, price) FROM '{cwd}/products.csv' DELIMITER ',' CSV HEADER"""
    try:
        await database.execute(query)
    except Exception as e:
        print(e)


async def add_order(n):
    customer_ids = await _get_customer_ids()
    product_ids = await _get_product_ids()
    for _ in range(n):
        customer_id = random.choice(customer_ids)
        order_date, ship_date = generate_order()
        query = insert(orders_table).values(
            customer_id=customer_id, order_date=order_date, ship_date=ship_date).returning('*')
        try:
            order_id = await database.execute(query)
            await add_order_items(order_id, product_ids)
        except Exception as e:
            print(e)


async def add_order_items(order_id, product_ids):
    for _ in range(1, random.randint(2, 4)):
        product_id = random.choice(product_ids)
        quantity = random.choices([1, 2, 3, 4], weights=[60, 25, 10, 5])[0]
        insert_query = insert(order_items).values(
            order_id=order_id, product_id=product_id, quantity=quantity)
        try:
            await database.execute(insert_query)
        except Exception as e:
            print(e)


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
