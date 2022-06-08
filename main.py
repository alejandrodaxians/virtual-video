from fastapi import FastAPI
from routes.film import film
from routes.rental import rental
from errors.errors import exception_handler_wrapper

description = """
## Virtual-video rental service includes two routes:

### Films

* Get all films
* Get all films by title coincidence
* Create films
* Delete a film by id
* Update a film by id

### Rental

* Check if a film is available for rent
* Rent a film
* Return a film

"""

app = FastAPI(
    title="Virtual-video Rental Service API",
    description=description,
)

app.include_router(film)
app.include_router(rental)

#handler for film not found
exception_handler_wrapper(app)

