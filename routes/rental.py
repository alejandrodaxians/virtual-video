from fastapi import APIRouter
from config.db import conn
from errors.errors import FilmNotFoundException, IdNotFoundException
from models.film_model import films_table
from schemas.film_schema import Film

rental = APIRouter()

#check if a film is rented, by name
@rental.get("/is_film_rented/", tags=["Check if a film is available for rent"])
async def is_film_rented(title_search: str):
    film_query = conn.execute(films_table.select().where(films_table.c.title.contains(title_search))).first()
    film_title = film_query[1]
    if film_query.rented:
        return ("\'" + film_title + "\'" + ", with id " + str(film_query[0]) + ", is rented")
    elif film_query.rented == False:
        return ("\'" + film_title + "\'" + ", with id " + str(film_query[0]) + ", is available for rent")

#set a film as rented, but if it's already set as rented return a message telling the user it can't be rented
@rental.put("/rent_film/{id}", tags=["Rent a film"])
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
@rental.put("/return_film/{id}", tags=["Return a film"])
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
