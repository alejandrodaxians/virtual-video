from fastapi import FastAPI
from app.routes.film import film
from app.routes.rental import rental
from app.errors.errors import exception_handler_wrapper
from starlette.responses import RedirectResponse

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

#handler for film or id not found
exception_handler_wrapper(app)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

