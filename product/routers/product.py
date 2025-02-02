from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from ..import models,schemas
from typing import List

router = APIRouter(
  tags=['Product'],
  prefix="/product"
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def addProduct(product:schemas.Product, db: Session = Depends(get_db)):
  new_product = models.Product(name=product.name,description=product.description,price=product.price, seller_id=product.seller_id)
  db.add(new_product)
  db.commit()               #changes will be saved to the database
  db.refresh(new_product)   #assign the id to the object which created by the database
  return new_product

@router.get('/', response_model = List[schemas.DisplayProduct])
def getAllProducts(db: Session = Depends(get_db)):
  products = db.query(models.Product).all()
  return products

@router.get('/{id}', response_model = schemas.DisplayProduct,status_code=status.HTTP_200_OK)
def findById(id:int, db:Session = Depends(get_db)):
  product = db.query(models.Product).filter(models.Product.id==id).first()
  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Product Not Found')
  return product

@router.delete('/delete/{id}')
def deleteById(id:int, db:Session = Depends(get_db)):
  db.query(models.Product).filter(models.Product.id==id).delete(synchronize_session=False)
  db.commit()
  return 'Product Deleted'

@router.put('/{id}')
def update(id:int, request: schemas.Product, db:Session = Depends(get_db)):
  product = db.query(models.Product).filter(models.Product.id == id)
  if not product.first():
    pass
  product.update(request.dict())
  db.commit()
  return "Product Updated"