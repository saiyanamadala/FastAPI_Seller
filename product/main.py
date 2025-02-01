from fastapi import FastAPI
from .import schemas
from .import models
from .database import engine

app = FastAPI()

models.database.Base.metadata.create_all(engine)   # This creates table in the database

@app.post('/product')
def addProduct(product:schemas.Product):
  return product