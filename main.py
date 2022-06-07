from fastapi import FastAPI
from routes.film import film
from routes.rental import rental
from errors.errors import exception_handler_wrapper

app = FastAPI()

app.include_router(film)
app.include_router(rental)

#handler for film not found
exception_handler_wrapper(app)

