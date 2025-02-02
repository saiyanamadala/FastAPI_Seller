from fastapi import FastAPI
from .import models
from .database import engine
from .routers import product,seller,login

app = FastAPI(
  title="Products API",
  description="Get details for all the products and sellers",
  terms_of_service="https://www.google.com",
  contact ={
    "Developer name" : "Sairam",
    "email": "sai@gmail.com"
  },
  license_info={
    "name": "license_name",
    "url" : "http://www.google.com"
  },
  docs_url="/documentation",
  redoc_url=None
)

app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)

models.database.Base.metadata.create_all(engine)   # This creates table in the database


