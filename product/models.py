from sqlalchemy import Column, Integer, String
from .import database

class Product(database.Base):
  __tablename__='products'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  description = Column(String)
  price = Column(Integer)