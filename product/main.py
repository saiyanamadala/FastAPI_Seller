from fastapi import FastAPI
from .import schemas

app = FastAPI()

@app.post('/product')
def addProduct(product:schemas.Product):
  return product