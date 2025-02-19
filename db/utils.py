from db import models
from db.engine import engine

def create_database():
    models.Base.metadata.create_all(engine)

def drop_database():
    models.Base.metadata.drop_all(engine)

def reset_database():
    drop_database()
    create_database()