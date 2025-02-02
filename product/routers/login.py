from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..import schemas, database, models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "f8dd6d48359c04e045bf43dec30c4a9973a318826fff46e9d83d0c362da249fb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20     # 20 minutes

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def generate_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):       #OAuth2PasswordRequestForm = Depends()
  user = db.query(models.Seller).filter(models.Seller.username == request.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username")
  if not pwd_context.verify(request.password, user.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password")
  access_token = generate_token(
    data={"sub": request.username}
  )
  return [{"access_token": access_token, "token_type": "bearer"}]

def get_current_user(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid auth credentials",
    headers={'WWW-Authenticate': "Bearer"},
  )
  try:
    payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    username: str = payload.get('sub')
    if username is None:
      raise credentials_exception
    token_data = schemas.TokenData(username=username)
  except JWTError:
    raise credentials_exception
  return token_data
