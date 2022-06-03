from fastapi import FastAPI, Query, Path
from pydantic import BaseModel

app = FastAPI()

#films dict for testing
films = {
    1: {
        "title": "Star Wars Episode IV: A New Hope",
        "genre": "Science Fiction",
        "year": 1977,
        "rented": False,
    }
}

#film model
class Film(BaseModel):
    title: str
    genre: str
    year: int
    rented: bool

#create film
@app.post("/films/{film_id}")
def create_film(film_id: int, film: Film):
    if film_id not in films:
        films[film_id] = film
        return {"message": f"Film with id {film_id} created"}
    else:
        return {"message": f"Film with id {film_id} already exists"}

#get film by id
@app.get("/films/{film_id}")
def get_film_by_id(film_id: int):
    if film_id in films:
        return films[film_id]
    else:
        return {"message": f"Film with id {film_id} not found"}

#get all films created
@app.get("/films")
def get_all_films():
    return films

#delete a film by id
@app.delete("/films/{film_id}")
def delete_film(film_id: int):
    if film_id in films:
        del films[film_id]
        return {"message": f"Film with id {film_id} deleted"}
    else:
        return {"message": f"Film with id {film_id} does not exist"}

#check if a film is rented or not, by name
@app.get("/films/{film_name}/rented")
def is_film_rented(film_name: str):
    for film in films.values():
        if film["title"] == film_name:
            if film["rented"]:
                return {"message": f"{film_name} is rented"}
            else:
                return {"message": f"{film_name} is not rented"}
    return {"message": f"Film {film_name} not found"}

#rent a film
@app.put("/films/{film_id}/rented")
def rent_film(film_id: int):
    if film_id in films:
        if films[film_id]["rented"] == True: 
            return {"message": f"Film with id {film_id} is already rented"}
        else:
            films[film_id]["rented"] = True
            return {"message": f"Film with id {film_id} is now rented by you"}
    else:
        return {"message": f"Film with id {film_id} not found"}

#return a film rented by you
@app.put("/films/{film_id}/return")
def return_film(film_id: int):
    if film_id in films:
        if films[film_id]["rented"] == False:
            return {"message": f"Film with id {film_id} is not rented"}
        else:
            films[film_id]["rented"] = False
            return {"message": f"Film with id {film_id} is now returned"}
    else:
        return {"message": f"Film with id {film_id} not found"}
    

