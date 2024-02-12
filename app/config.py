from pydantic import BaseModel, Field

# Define your desired data structure.
class CurrencyConvertModel(BaseModel):
    amount: str = Field(description="amount to be converted")
    currency_from: str = Field(description="currency to be converted from")
    currency_to: str = Field(description="currency to be converted to")

class QueryBody(BaseModel):
    query: str = Field(description="query for conversion")

class EventBody(BaseModel):
    event_name: str = Field(description="event name")
    event_data: dict = Field(description="event parameters")
    timestamp: str = Field(description="timestamp")
