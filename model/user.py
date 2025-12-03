from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from model.product import Product
from extensions import db  # Importa o db globalmente definido

class User(db.Model):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    date_created = Column(DateTime, default=datetime.now())

    products = relationship("Product", back_populates="owner")
    comments = relationship("Comment", back_populates="author")