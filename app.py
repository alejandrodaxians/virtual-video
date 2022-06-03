from fastapi import FastAPI
from routes.film import film

app = FastAPI()

app.include_router(film)