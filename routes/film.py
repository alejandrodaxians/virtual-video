from urllib import response
from fastapi import APIRouter, HTTPException
from config.db import conn
from models.film_model import films_table
from schemas.film_schema import Film

film = APIRouter()

#get all films from the database
@film.get("/get_all_films", tags=["Get all films"])
async def get_all_films():
    return conn.execute(films_table.select()).fetchall()

#get a film by title, where the string passed by the user is a substring of the title
@film.get("/get_film_by_title", tags=["Get all films by title coincidence"])
async def get_film_by_title(title_search: str):
    result = conn.execute(films_table.select().where(films_table.c.title.contains(title_search))).fetchall()
    if result == []:
        return HTTPException(status_code=404, detail="Film not found")
    else:
        return result

#create a film on the table
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
@film.delete("/delete_film/{id}", tags=["Delete a film by id"])
async def delete_film(id: int):
    if id not in films_table:
        return HTTPException(status_code=404, detail="Film not found")
    else:
        result = conn.execute(films_table.select().where(films_table.c.id == id)).fetchall()
        film_title = result[0][1]
        conn.execute(films_table.delete().where(films_table.c.id == id))
        return {"message": "Film with title: " + film_title + ", deleted"}

#update a film's information, with every field being optional
@film.put("/update_film/{id}", tags=["Update a film by id"])
async def update_film(id: int, film: Film):
        query = films_table.update().where(films_table.c.id == id).values(
            title=film.title,
            year=film.year,
            rented=film.rented
        )
        conn.execute(query)
        return conn.execute(films_table.select().where(films_table.c.id == id)).first()

#check if a film is rented, by name
@film.get("/is_film_rented/", tags=["Check if a film is available for rent"])
async def is_film_rented(title_search: str):
    film_query = conn.execute(films_table.select().where(films_table.c.title.contains(title_search))).first()
    film_title = film_query[1] 
    if film_query.rented:
        return ("Film  with title: " + film_title + ", is unavailable")
    else:
        return ("Film with title: " + film_title + ", is available")

