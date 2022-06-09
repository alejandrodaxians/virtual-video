from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:mysql24601@localhost:3306/filmsdb")

meta = MetaData()

conn = engine.connect()

