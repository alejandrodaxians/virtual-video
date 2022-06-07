from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

class FilmNotFoundException(Exception):
    def __init__(self, name: str):
        self.title_search = name

class IdNotFoundException(Exception):
    def __init__(self, id: int):
        self.id = id

def exception_handler_wrapper(app: FastAPI):
    @app.exception_handler(FilmNotFoundException)
    async def film_exception_handler(request: Request, exc: FilmNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"message": f"No coincidences found with {exc.title_search}"},
        )

    @app.exception_handler(IdNotFoundException)
    async def id_exception_handler(request: Request, exc: IdNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"message": f"No film with id {exc.id} found"},
        )