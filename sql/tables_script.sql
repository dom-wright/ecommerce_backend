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