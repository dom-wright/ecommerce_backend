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
    Numeric,
    Boolean
)


# DATABASES
DATABASE_URL = 'postgresql+asyncpg://localhost:5432/my_orders_db'
database = Database(DATABASE_URL)

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(length=100)),
    Column("hashed_password", String(length=100)),
    Column("full_name", String(length=100)),
    Column("email", String(length=100)),
    Column("is_superuser", Boolean),
    Column("is_staff", Boolean),
    Column("is_active", Boolean),
    Column("date_joined", DateTime),
    Column("address", String(length=100)),
    Column("county", String(length=100))
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
    Column("user_id", Integer, ForeignKey(
        "users.id")),
    Column("order_date", DateTime),
    Column("ship_date", Date),
    Column("order_status", String(length=100))
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
