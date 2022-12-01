from databases import Database
from sqlalchemy import (
    ForeignKey,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    DateTime,
    Date,
    Numeric
)


# DATABASES
DATABASE_URL = 'postgresql+asyncpg://localhost:5432/my_orders_db'
database = Database(DATABASE_URL)

metadata = MetaData()

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

order_items_table = Table(
    "order_items",
    metadata,
    Column("order_id", Integer, ForeignKey(
        "orders.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey(
        "products.id"), primary_key=True),
    Column("product_unit_price", Numeric(precision=10, scale=2)),
    Column("quantity", Integer)
)
