CREATE TABLE
  IF NOT EXISTS products (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_sku uuid NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    product_name varchar(100) NOT NULL,
    product_category varchar(100),
    price money NOT NULL CHECK(price :: numeric > 0)
  );


CREATE TABLE
  IF NOT EXISTS customers (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_name varchar(100) NOT NULL,
    address varchar(100) NOT NULL,
    county varchar(100) NOT NULL,
    email varchar(100) NOT NULL UNIQUE
  );


CREATE TABLE
  IF NOT EXISTS orders (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id integer REFERENCES customers(id) NOT NULL,
    order_date timestamp NOT NULL DEFAULT NOW(),
    order_status varchar(100) NOT NULL CHECK(
      order_status in (
        'Pending',
        'Accepted',
        'Cancelled',
        'Dispatched',
        'Delivered'
      )
    ) DEFAULT 'Pending',
    ship_date date CHECK(order_status = 'Delivered')
  );


CREATE TABLE
  IF NOT EXISTS order_items (
    order_id integer REFERENCES orders(id) ON DELETE CASCADE,
    product_id integer REFERENCES products(id),
    product_unit_price money NOT NULL CHECK(product_unit_price :: numeric > 0),
    quantity integer NOT NULL CHECK(quantity > 0),
    PRIMARY KEY (order_id, product_id)
  );