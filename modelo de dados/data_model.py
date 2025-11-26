from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from data_model import Base, Comment



class Product(Base) {
    __tablename__ = 'product'

    id = Column("pk_product", Integer, primary_key=True)
    name = Column(String(140), unique=True)
    date_inserted = Column(DateTime, default=datetime.now())
    barcode = Column(Integer, unique=True)
    ## ver outras propriedades do produto na API do Open Food Facts
    # relacionamento do objeto Product com o Comment
    comments = relationship("Comment")

}

def _init__(self, name:str, barcode:int,
             date_inserted:Union[DateTime, None] = None):
    """
    Cria um Product

    Arguments:
        name: nome do produto.
        barcode: código de barras do produto
        date_inserted: data de quando o produto foi inserido à base
    """
    self.name = name
    self.barcode = barcode

    # se não for informada, será o data exata da inserção no banco
    if date_inserted:
        self.date_inserted = date_inserted

