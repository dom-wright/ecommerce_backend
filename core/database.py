from databases import Database
from sqlalchemy import (
    create_engine,
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
# engine = create_engine(DATABASE_URL)

customers_table = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(length=100)),
    Column("address", String(length=100)),
    Column("email", String(length=100))
)

customers_table = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("product_sku", String(length=32)),
    Column("product_name", String(length=100)),
    Column("product_category", String(length=100)),
    Column("price", Numeric(precision=10, scale=2))
)

customers_table = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("product_id", Integer),
    Column("customer_id", Integer),
    Column("order_price", Numeric(precision=10, scale=2)),
    Column("quantity", Integer),
    Column("total_price", Numeric(precision=10, scale=2)),
    Column("order_date", DateTime),
    Column("ship_date", Date),
)


'''
CREATE TABLE
  IF NOT EXISTS products (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_sku uuid NOT NULL UNIQUE,
    product_name varchar(100) NOT NULL,
    product_category varchar(100),
    price money NOT NULL CHECK(price :: numeric > 0)
  );


CREATE TABLE
  IF NOT EXISTS customers (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_name varchar(100) NOT NULL,
    address varchar(100) NOT NULL,
    email varchar(100) NOT NULL UNIQUE
  );


CREATE TABLE
  IF NOT EXISTS orders (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id integer REFERENCES products(id),
    customer_id integer REFERENCES customers(id),
    order_price money NOT NULL CHECK(order_price :: numeric > 0),
    quantity integer NOT NULL CHECK(quantity > 0),
    total_price money NOT NULL CHECK(total_price :: numeric > 0),
    order_date timestamp DEFAULT NOW(),
    ship_date date
  );
  '''
