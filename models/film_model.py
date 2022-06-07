from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from config.db import meta, engine

films_table = Table('films', meta, 
    Column("id", Integer, primary_key=True), 
    Column("title", String(255)), 
    Column("year", Integer), 
    Column("rented", Boolean))

meta.create_all(engine)