from fastapi import APIRouter
from app.config.db import conn
from app.errors.errors import FilmNotFoundException, IdNotFoundException
from app.models.film_model import films_table
from app.schemas.film_schema import Film, FilmUpdate

film = APIRouter()

#get all films from the database
#tested
@film.get("/films", 
    tags=["Films"], 
    summary="Get all films", 
    description="Output all films currently in the database, ordered by id."
    )
async def get_all_films():
    return conn.execute(films_table.select()).fetchall()

#get a film by title, where the string passed by the user is a substring of the title
#tested
@film.get("/films/get_film_by_title", 
    tags=["Films"],
    summary="Get films by title",
    description="Input a keyword and output all films that contain that keyword in their title. If there are no films with that keyword, an error is returned.",
    )
async def get_film_by_title(keyword: str):
    result = conn.execute(films_table.select().where(films_table.c.title.contains(keyword))).fetchall()
    if result == []:
        raise FilmNotFoundException(keyword)
    else:
        return result

#create a film on the table
#tested
@film.post("/films/create_film", 
    tags=["Films"],
    summary="Create a film",
    description="Input a title and a year and create a new film. The id will be automatically assigned, and it will be set as available for rent by default.",
    )
async def create_film(film: Film):
    query = films_table.insert().values(
        title=film.title,
        year=film.year
    )
    conn.execute(query)
    return film
    
#delete a film by id, returning a message if the id is not on the table
#tested
@film.delete("/films/delete_film/{id}", 
    tags=["Films"],
    summary="Delete a film",
    description="Input an id and delete the film with that id. If the id is not on the database, a message will be returned.",
    )
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
@film.put("/films/update_film/{id}", 
    tags=["Films"],
    summary="Update a film",
    description="Input an id and a title and update the film with that id. If the id is not on the database, a message will be returned.",
    )
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
        