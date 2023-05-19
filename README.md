# 🛒 Ecommerce API 🛒

## What is this?
An API backend for an ecommerce app. The API defines a series of endpoints for managing customers, products, and orders. The app uses the FastAPI Python web framework and PostgreSQL RDBMS.

### Why?
Much of my experience before this project was creating full-stack web applications with Django. Django comes 'batteries included', with excellent tools that abstract away the complexity of common tasks, such as its ORM for database management, auth packages, class-based views, and templating support. This project was an opportunity to set aside the safety net of these features, learn a new Python framework, and generally get closer to the code driving these applications.

### Declarations
- This project is highly simplified, and lacks important features. It is not intended to be production ready.
- I chose FastAPI as it is lightweight, with many interesting features not automatically available as part of Django's standard distribution, including asynchronous support, type hints and validation, and automated generation of API documentation.
- SQLAlchemy Core was purposely used over SQLAlchemy ORM in order to remain closer to the SQL code. If intended for production, ORM and migrations packages would be key tools.

- - -

## Instructions for setup
You must have PostgreSQL installed on your machine. [Postgres website](https://www.postgresql.org/download/).

### Clone Project
1. Clone this repository to your local machine.
2. `cd` into `ecommerce_backend`.
3. Create a virtual environment using the tools of your choice.
4. Install dependencies by running `pip install -r requirements.txt`

### Database setup
5. Open up the command line in the current directory (/ecommerce_backend). Run the `psql` command to open up an interactive shell connected with the PostgreSQL server. Inside the shell, copy, paste and execute the following commands:
    ```
    CREATE DATABASE orders_api_db;
    \c orders_api_db
    \i src/db/setup.sql
    \q
    ```

### Run
6. Run `uvicorn src.main:app --reload` in the terminal to start the Uvicorn server with automatic code reloading. The application should now be up and running at `localhost:8000`. Visting this URL will bring up the home page. Entering your name will render a button linking to the docs where you can test out the endpoints, or you can just go straight there at http://localhost:8000/docs.

### Data
7. Now we have reached the docs page, we can give our API a test ride. At the moment the application has no data in it, so let's fill it with some! Scroll to the `Admin` section at the bottom of the docs page, select the `/admin/create` endpoint and hit `Try it out`.

   - **Products**: First select `products` from the drop down, and then click `execute`.
   - **Users**: Switch the value in the drop down to users, type in the number of users you would like to create, then click `execute`. All users have the same password 'password'.
   - **Orders**: Finally switch the value in the drop down to orders, type in the number of orders you would like to create, and finally click `execute`.

    Note that product data is contained in a CSV file which the application will automatically ingest it into the `products` table. The code being activated by these requests can be found in `src/db/data_generation.py`.

### Authentication & Authorization
For access to most endpoints you will need to register an account and login. Process:
1. Create an account through the `/auth/register/` endpoint in the Auth section.
2. Click on the `Authorize` button in the top right and login. This will automatically add the JWT token to the `Authorize` header on every request.
