from fastapi import APIRouter, HTTPException 
from config.db import conn
from errors.errors import FilmNotFoundException, IdNotFoundException
from models.film_model import films_table
from schemas.film_schema import Film, FilmUpdate

film = APIRouter()

#get all films from the database
#tested
@film.get("/get_all_films", tags=["Get all films"])
async def get_all_films():
    return conn.execute(films_table.select()).fetchall()

#get a film by title, where the string passed by the user is a substring of the title
#tested
@film.get("/get_film_by_title", tags=["Get all films by title coincidence"])
async def get_film_by_title(title_search: str):
    result = conn.execute(films_table.select().where(films_table.c.title.contains(title_search))).fetchall()
    if result == []:
        raise FilmNotFoundException(title_search)
    else:
        return result

#create a film on the table
#tested
@film.post("/create_film", tags=["Create a new film"])
async def create_film(film: Film):
    query = films_table.insert().values(
        title=film.title,
        year=film.year,
        rented=film.rented
    )
    conn.execute(query)
    return film
    
#delete a film by id, returning a message if the id is not on the table
#tested
@film.delete("/delete_film/{id}", tags=["Delete a film by id"])
async def delete_film(id: int):
    exists = conn.execute(films_table.select().where(films_table.c.id == id)).first()
    if exists == None:
        raise IdNotFoundException(id)
    else:
        result = conn.execute(films_table.select().where(films_table.c.id == id)).fetchall()
        film_title = result[0][1]
        conn.execute(films_table.delete().where(films_table.c.id == id))
        return {"message": "Film with title: " + film_title + ", deleted"}

#update a film's information. If no value is passed, the value will remain the same as it were before
#tested
@film.put("/update_film/{id}", tags=["Update a film"])
async def update_film(id: int, film: FilmUpdate):
    exists = conn.execute(films_table.select().where(films_table.c.id == id)).first()
    if exists == None:
        raise IdNotFoundException(id)
    else:
        query = films_table.update().where(films_table.c.id == id).values(
            title=film.title if film.title != None else exists.title,
            year=film.year if film.year != None else exists.year
        )
        conn.execute(query)
        return conn.execute(films_table.select().where(films_table.c.id == id)).first()
        