# 🛒 Ecommerce API 🛒

### What is this?
An API backend for an ecommerce app. The API defines a series of endpoints for managing customers, products, and orders. The app uses the FastAPI Python web framework and PostgreSQL RDBMS.

### Why?
Much of my experience before this project was creating full-stack web applications with Django. Django comes 'batteries included', with excellent tools that abstract away the complexity of common tasks, such as its ORM for database management, auth packages, class-based views, and templating support. This project was an opportunity to set aside the safety net of these features, learn a new Python framework, and generally get closer to the code driving these applications.

### Declarations
- This project was a learning / practice project. It is highly simplified, and lacks many key features to make it safe for production.
- I chose FastAPI as it is lightweight, with many interesting features not automatically available as part of Django's standard distribution, including asynchronous support, type hints and validation, and automated generation of API documentation.
- I used SQLAlchemy Core over SQLAlchemy ORM to stay closer to the SQL code (for practice). Utilising the ORM and migrations packages would otherwise be optimal.

- - -

## Instructions for setup

### Requirements
You must have PostgreSQL installed on your machine. [Postgres website](https://www.postgresql.org/download/).

### Clone Project
1. Clone this repository to your local machine.
2. `cd` into `ecommerce_backend`.
3. Create a virtual environment using the tools of your choice.
4. Install dependencies by running `pip install -r requirements.txt`.
5. Create a `.env` file inside the current directory. Inside it add a key-value pair with `SECRET_KEY` as the key and a suitable key value (running `openssl rand -hex 32` in the command line is helpful for creating secure keys).
   ```
   SECRET_KEY="2c834206cd5edbdd76..."
   ```

### Database setup
6. Open up the command line in the current directory (/ecommerce_backend). Run the `psql` command to open up an interactive shell connected to the PostgreSQL server. Inside the shell, copy, paste and execute the following commands:
    ```
    CREATE DATABASE orders_api_db;
    \c orders_api_db
    \i src/db/setup.sql
    \q
    ```

### Run
7. Run `uvicorn src.main:app --reload` in the terminal to start the Uvicorn server with automatic code reloading. The application should now be up and running at http://localhost:8000. Visit this URL and enter your name to reveal a button linking to the docs, or you can just go direct at http://localhost:8000/docs.

### Data
8. Now we have reached the docs page, we can give our API a test ride. At the moment the application has no data in it, so let's fill it with some! Scroll to the `Admin` section at the bottom of the docs page, select the `/admin/create` endpoint and click `Try it out`.

   - **Products**: First select `Products` from the drop down, then click `Execute`.
   - **Users**: Switch the value in the drop down to `Users`, type in the number of users you would like to create, then click `Execute`. All users have the same password `'password'`.
   - **Orders**: Finally switch the value in the drop down to `Orders`, type in the number of orders you would like to create, and click `Execute`.

    Note that the product data is contained in a CSV file, which the application will automatically ingest into the `products` table. The code being activated by these requests can be found in `src/db/data_generation.py`.

### Authentication & Authorization
For access to most endpoints you will need to register an account and login. Process:
8. Create an account through the `/auth/register/` endpoint in the Auth section.
9. Click on the `Authorize` button in the top right and login. This will automatically add the JWT token to the `Authorize` header for every subsequent request.
    
### Browse
Finally you are ready to test out the endpoints!
