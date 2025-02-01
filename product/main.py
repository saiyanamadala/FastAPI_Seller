from fastapi import FastAPI,status, Response, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .import schemas
from .import models
from .database import engine, sessionLocal
from typing import List

app = FastAPI()

models.database.Base.metadata.create_all(engine)   # This creates table in the database

def get_db():
  db=sessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.post('/product',status_code=status.HTTP_201_CREATED)
def addProduct(product:schemas.Product, db: Session = Depends(get_db)):
  new_product = models.Product(name=product.name,description=product.description,price=product.price)
  db.add(new_product)
  db.commit()               #changes will be saved to the database
  db.refresh(new_product)   #assign the id to the object which created by the database
  return new_product

@app.get('/products', response_model = List[schemas.DisplayProduct])
def getAllProducts(db: Session = Depends(get_db)):
  products = db.query(models.Product).all()
  return products

@app.get('/product/{id}', response_model = schemas.DisplayProduct,status_code=status.HTTP_200_OK)
def findById(id:int, db:Session = Depends(get_db)):
  product = db.query(models.Product).filter(models.Product.id==id).first()
  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Product Not Found')
  return product

@app.delete('/delete/{id}')
def deleteById(id:int, db:Session = Depends(get_db)):
  db.query(models.Product).filter(models.Product.id==id).delete(synchronize_session=False)
  db.commit()
  return 'Product Deleted'

@app.put('/product/{id}')
def update(id:int, request: schemas.Product, db:Session = Depends(get_db)):
  product = db.query(models.Product).filter(models.Product.id == id)
  if not product.first():
    pass
  product.update(request.dict())
  db.commit()
  return "Product Updated"