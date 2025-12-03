from extensions import db  # Importa o db globalmente definido
from datetime import datetime
from sqlalchemy.orm import relationship

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column("pk_product", db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    barcode = db.Column(db.Integer, unique=True)
    date_inserted = db.Column(db.DateTime, default=datetime.now())
    # ... outros campos

    comments = db.relationship("Comment", backref="product") # Usando db.relationship
