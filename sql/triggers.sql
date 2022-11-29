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