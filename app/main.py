import os
import json
import logging

import psycopg2
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import EventBody
from app.nlp_to_json import parse_unstructured_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
connection_parameters = {
    'user': os.getenv("POSTGRES_USER"),
    'password': os.getenv("POSTGRES_PASSWORD"),
    'host': "localhost",
    'port': "5432",
    'database': os.getenv("POSTGRES_DATABASE")}

connection = psycopg2.connect(**connection_parameters)
connection.autocommit = True

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/text_to_json")
async def query(query):
    """
    Example usage:
    curl -X GET "http://localhost:8000/text_to_json?query=example_query"
    """
    val = parse_unstructured_text(query)
    return JSONResponse(val["json"])

def event_handler(event, cursor, table_name):
    if table_name == 'webapp_events':
        # Convert the event_data dictionary to a JSON string
        event_data_json = json.dumps(event.event_data)

        # Construct the INSERT statement
        statement = f"INSERT INTO public.{table_name} (event_name, event_data, timestamp) VALUES ('{event.event_name}', '{event_data_json}', '{event.timestamp}')"
    
    cursor.execute(statement)
    logger.info(f"executed: {statement}")

@app.post("/log")
async def log_event(event: EventBody):
    """
    Example usage:
    curl -X POST "http://localhost:8000/log" \
    -H "Content-Type: application/json" \
    -d '{
        "event_name": "login",
        "event_data": {"user": "jojo@gmail.com", "device": "Iphone 22"},
        "timestamp": "2022-01-01T00:00:00Z"
    }'
    """

    try:
        with connection.cursor() as cursor:
            event_handler(event, cursor, 'webapp_events')
    except Exception as e:
        print(e)

...
