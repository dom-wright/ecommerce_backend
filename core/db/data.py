from datetime import datetime, timedelta
import random
from faker import Faker


counties = [
    'Greater London', 'Strathclyde', 'West Lothian', 'North Yorkshire', 'Surrey',
    'Kent', 'Essex', 'Lancashire', 'Durham', 'Glamorgan', 'Cornwall', 'Anglesey', 'Highlands'
]

numbers = [1, 2, 3, 4, 5, 6, 7]

fake = Faker(locale='en_GB')


def generate_customer():
    first_name = fake.first_name()
    last_name = fake.last_name()
    name = f'{first_name} {last_name}'
    raw_address = fake.address()
    address = raw_address.replace('\n', ', ').rsplit(', ', 1)[0]
    county = random.choices(counties, weights=(
        30, 10, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5))[0]
    email = f'{first_name}.{last_name}@{fake.domain_name()}'
    return name, address, county, email


def generate_order():
    random_time_delta = timedelta(days=random.randrange(0, 180), hours=random.randrange(
        0, 24), minutes=random.randrange(0, 60), seconds=random.randrange(0, 60))
    order_date = datetime.now() - random_time_delta
    days_to_delivery = timedelta(days=random.choices(
        numbers, weights=[15, 25, 20, 15, 10, 10, 5])[0])
    if days_to_delivery > random_time_delta:
        ship_date = None
    else:
        ship_datetime = order_date + days_to_delivery
        ship_date = ship_datetime.date()
    return order_date, ship_date
