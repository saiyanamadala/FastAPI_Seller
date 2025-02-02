from fastapi import APIRouter, Depends, HTTPException, status
from ..import schemas, database, models
from passlib.context import CryptContext
from sqlalchemy.orm import Session

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
  user = db.query(models.Seller).filter(models.Seller.username == request.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username")
  if not pwd_context.verify(request.password, user.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password")
  
  return request
