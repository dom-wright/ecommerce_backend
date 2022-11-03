-- TRIGGER FOR FORCING AUTO UUID ON NEW PRODUCTS.
CREATE
OR REPLACE FUNCTION force_uuid() RETURNS trigger AS $$
BEGIN NEW.product_sku: = gen_random_uuid();
RETURN NEW;
END $$ LANGUAGE plpgsql;


CREATE TRIGGER
  force_uuid BEFORE
INSERT
  ON products FOR EACH ROW
EXECUTE
  FUNCTION force_uuid();


-- TRIGGER FOR SETTING UNIT PRICE AT TIME OF ORDER & CALCULATING TOTAL.
CREATE
OR REPLACE FUNCTION calculate_total() RETURNS trigger AS $$
BEGIN
  NEW.order_price = (
  SELECT
    price
  FROM
    products
  WHERE
    id = NEW.product_id;
  )
  NEW.total_price := NEW.quantity * NEW.order_price
  RETURN NEW;
END $$ LANGUAGE plpgsql;


CREATE TRIGGER
  calculate_total BEFORE
INSERT
  ON orders FOR EACH ROW
EXECUTE
  FUNCTION calculate_total();