/app/models: Contains the SQLAlchemy models that represent your database tables.

/app/schemas: Contains Pydantic models (schemas) that define the data validation for requests and responses.

/app/crud: Contains the actual database logic for CRUD (Create, Read, Update, Delete) operations.

/app/core: Contains configuration files, utility functions, and constants (e.g., the database URL).

main.py: The entry point of your FastAPI app where we define the routes and include the dependencies.