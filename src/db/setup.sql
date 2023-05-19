CREATE TABLE
  IF NOT EXISTS products (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_sku uuid NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    product_name varchar(100) NOT NULL,
    product_category varchar(100),
    price money NOT NULL CHECK(price :: numeric > 0)
  );


CREATE TABLE
  IF NOT EXISTS users (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username varchar(100) NOT NULL,
    hashed_password varchar(100) NOT NULL,
    full_name varchar(100) NOT NULL,
    email varchar(100) NOT NULL UNIQUE,
    is_superuser boolean NOT NULL DEFAULT 'f',
    is_staff boolean NOT NULL DEFAULT 'f',
    is_active boolean NOT NULL DEFAULT 't',
    date_joined timestamp NOT NULL DEFAULT NOW(),
    address varchar(100) NOT NULL,
    county varchar(100) NOT NULL
  );


CREATE TABLE
  IF NOT EXISTS orders (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer REFERENCES users(id) ON DELETE
    SET
      NULL,
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
      ship_date date
  );


CREATE TABLE
  IF NOT EXISTS order_items (
    order_id integer REFERENCES orders(id) ON DELETE CASCADE,
    product_id integer REFERENCES products(id),
    product_unit_price money NOT NULL CHECK(product_unit_price :: numeric > 0),
    quantity integer NOT NULL CHECK(quantity > 0),
    PRIMARY KEY (order_id, product_id)
  );


-- TRIGGER FOR SETTING UNIT PRICE AT TIME OF ORDER.
CREATE
OR REPLACE FUNCTION set_order_unit_price() RETURNS trigger AS $$
BEGIN
  NEW.product_unit_price := (
  SELECT
    price
  FROM
    products
  WHERE
    id = NEW.product_id
  );
  RETURN NEW;
END $$ LANGUAGE plpgsql;


CREATE TRIGGER
  set_order_unit_price BEFORE
INSERT
  ON order_items FOR EACH ROW
EXECUTE
  FUNCTION set_order_unit_price();