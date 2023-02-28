from fastapi import FastAPI
from routers import seller,product,login
import models
from database import Base,engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(seller.router)
app.include_router(product.router)
app.include_router(login.router)