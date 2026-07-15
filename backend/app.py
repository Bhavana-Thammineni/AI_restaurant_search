from fastapi import FastAPI
from restaurant_service import get_restaurants

app = FastAPI()


@app.get("/restaurants/{location}")
def restaurants(location: str):
    return get_restaurants(location)