from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from fastapi import FastAPI
from sqlalchemy.orm import relationship

class Seller(Base):
    __tablename__ = "sellers"
    seller_unique_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    
    seller = relationship("Product", back_populates="owner")


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    seller_id = Column(Integer, ForeignKey("sellers.seller_unique_id"))

    owner = relationship("Seller", back_populates="seller")
