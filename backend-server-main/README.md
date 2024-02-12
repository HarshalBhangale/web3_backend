# Description
Contains AI code to convert a message into json

# to start server

    poetry install
    poetry run uvicorn app.main:app --reload 

# Routes

    POST /query
    Body: { query: "Please convert 100 USDT to ETH" }

# Database
1. Create user:
    ```
    create user solsuit with password 'solsuiter@42';
    CREATE ROLE event_creator with login password 'solsuiter@42';
    ALTER USER solsuit CREATEDB;
    GRANT ALL PRIVILEGES ON DATABASE solsuit_db TO solsuit;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO solsuit;
    ```

2. 