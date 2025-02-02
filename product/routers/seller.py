from fastapi import APIRouter
from passlib.context import CryptContext
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..import models,schemas
from ..database import get_db

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/addSeller', response_model=schemas.DisplaySeller, tags=['Seller'])
def addSeller(seller: schemas.Seller, db:Session = Depends(get_db)):
  hashedPassword = pwd_context.hash(seller.password)
  new_seller = models.Seller(username=seller.username,email=seller.email,password=hashedPassword)
  db.add(new_seller)
  db.commit()
  db.refresh(new_seller)
  return new_seller