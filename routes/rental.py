from fastapi import APIRouter
from config.db import conn
from errors.errors import FilmNotFoundException, IdNotFoundException
from models.film_model import films_table
from schemas.film_schema import Film

rental = APIRouter()

#check if a film is rented, by name
@rental.get("/rental/is_film_rented/", 
        tags=["Rental"],
        summary="Check if a film is rented",
        description="Input a title and check if the film is rented or if it's available for rent.",
        )
async def is_film_rented(keyword: str):
    film_query = conn.execute(films_table.select().where(films_table.c.title.contains(keyword))).first()
    if film_query.rented:
        film_title = film_query[1]
        return ("\'" + film_title + "\'" + ", with id " + str(film_query[0]) + ", is rented and unavailable.")
    else:
        film_title = film_query[1]
        return ("\'" + film_title + "\'" + ", with id " + str(film_query[0]) + ", is available for rent")

#set a film as rented, but if it's already set as rented return a message telling the user it can't be rented
@rental.put("/rental/rent_film/{id}", 
        tags=["Rental"],
        summary="Rent a film",
        description="Input an id and rent the film with that id. If the id is not on the database, a message will be returned, and if the film is already rented, a message will be returned.",
        )
async def rent_film(id: int):
    film_query = conn.execute(films_table.select().where(films_table.c.id == id)).first()
    if film_query == None:
        raise IdNotFoundException(id)
    elif film_query.rented:
        film_title = film_query[1]
        return ("\'" + film_title + "\'" + ", with id " + str(film_query[0]) + ", is already rented")
    else:
        film_title = film_query[1]
        query = films_table.update().where(films_table.c.id == id).values(rented=True)
        conn.execute(query)
        return ("You have rented " + "\'" + film_title + "\'")

#return a film, but if it's already set as available return a message telling the user it can't be returned
@rental.put("/rental/return_film/{id}", 
        tags=["Rental"],
        summary="Return a film",
        description="Input an id and return the film with that id. If the id is not on the database, a message will be returned, and if the film is already available, a message will be returned.",
        )
async def return_film(id: int):
    film_query = conn.execute(films_table.select().where(films_table.c.id == id)).first()
    if film_query == None:
        raise IdNotFoundException(id)
    elif film_query.rented == False:
        film_title = film_query[1]
        return ("\'" + film_title + "\' is available for rent, it can't be returned")
    elif film_query.rented:
        film_title = film_query[1]
        query = films_table.update().where(films_table.c.id == id).values(rented=False)
        conn.execute(query)
        return ("You have returned " + "\'" + film_title + "\'")
    else:
        raise IdNotFoundException(id)
