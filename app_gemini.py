# app.py (Gabarito Final)
from flask import Flask, jsonify
from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote
import os

# Importa o db globalmente definido (deve estar em extensions.py)
from extensions import db 

# Importa os modelos para que db.create_all() os encontre
from model.product import Product 
from model.user import User 
from model.comment import Comment

# ====================================================================
# 2. APPLICATION FACTORY: FUNÇÃO CREATE_APP
# ====================================================================

def create_app(config_name='development'):
    """
    Cria e configura a instância da aplicação Flask.
    'testing' usa o SQLite em memória.
    """
    # Usando OpenAPI como base do App (conforme seu original)
    app = OpenAPI(__name__) 
    
    # ------------------ Configuração do DB ------------------
    if config_name == 'testing':
        # SQLite em memória para testes
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        app.config['TESTING'] = True
    else:
        # SQLite em arquivo (Desenvolvimento/Produção)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///antigreenwashing.db' 

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # VINCULA o objeto 'db' ao App
    db.init_app(app)
    
    # CRIA AS TABELAS: Precisa estar dentro do contexto da aplicação
    with app.app_context():
        # db.create_all() usa os modelos Product, User, Comment, etc.
        db.create_all()

    # ------------------ 3. ROTAS (Endpoints) ------------------
    
    # 1 - endpoint to check if the server is running
    @app.route('/')
    def home():
        return "Welcome!"

    # adicionar o endpoint de adicionar produto (C DO CRUD)
    @app.post('/add_product', tags=[product_tag],
            responses={"200": ProductViewSchema, "409": ErrorSchema, "400": ErrorSchema}  )
    def add_product(form: ProductSchema):
        """ Adds a new product to the data base """
        
        # Cria a instância do modelo, usando form.name e form.barcode
        product = Product(
            name=form.name,
            barcode=form.barcode,
            comment=form.comment,
            sustainable_seals=form.sustainable_seals,
        )
        logger.debug(f"Adding a product: '{product.name}'")

        try:
            # Usando db.session.add e db.session.commit (gerenciado pelo Flask-SQLAlchemy)
            db.session.add(product)
            db.session.commit()
            logger.debug(f"Product added successfully: '{product.name}'")
            return product, 200 
        
        except IntegrityError as e:
            db.session.rollback() # ✅ Rollback em caso de erro
            error_msg = "Product is already in the data base"
            logger.warning(f"Error adding '{product.name}': {error_msg}")
            return {"message": error_msg}, 409
        
        except Exception as e:
            db.session.rollback()
            error_msg = "Could not add the product"
            logger.warning(f"Erro: {error_msg}")
            return {"message": error_msg}, 400


    @app.get('/product', tags=[product_tag],
         responses={"200": ProductViewSchema, "404": ErrorSchema})
    def get_produto(query: ProdutoSearchSchema):
        """Search for a product in the local data base"""
        product_name = query.name
        logger.debug(f"Searching product locally: '{product_name}'")
        
        # Usando a interface de query do Flask-SQLAlchemy (Product.query)
        product = Product.query.filter(
            Product.name == product_name
        ).first() # .first() substitui o .first() do Session

        
        if not product:
            error_msg = "Product not found."
            logger.warning(f"'{product_name}' not found")
            return {"message": error_msg}, 404
        
        logger.debug(f"Product found: '{product.name}'")
        return product, 200 # Retorna o objeto encontrado


    # 3 - endpoint to get product details by barcode (Placeholder)
    @app.get('/product_by_barcode')
    def get_product_by_barcode():
        return jsonify({"message": "Endpoint para buscar produto por barcode (TO DO)"})

    # 4 - endpoint to get product history (placeholder)
    @app.get('/api/products_history')
    def get_products_history():
        return jsonify({"message": "Product history endpoint"})

    @app.delete('/produto', tags=[product_tag],
                responses={"200": ProductDelSchema, "404": ErrorSchema})
    def del_produto(query: ProductBuscaSchema):
        """Deleta produto por nome"""
        product_name = unquote(unquote(query.name))
        logger.debug(f"Deletando produto: '{product_name}'")
        
        try:
            # Usando o Product.query.filter e o delete()
            count = Product.query.filter(
                Product.name == product_name
            ).delete()
            db.session.commit() # Commit para efetivar a deleção
            
            if count:
                logger.debug(f"Product '{product_name}' deleted")
                return {"message": "Produto removed", "name": product_name}, 200
            else:
                error_msg = "Produto não encontrado"
                logger.warning(f"'{product_name}' não encontrado para deletar")
                return {"message": error_msg}, 404
                
        except Exception as e:
            db.session.rollback()
            error_msg = "Could not delete the product"
            logger.warning(f"Erro na deleção: {error_msg}")
            return {"message": error_msg}, 400
            
    return app


# ====================================================================
# 4. EXECUÇÃO
# O bloco principal chama o App Factory para iniciar a aplicação
# ====================================================================
if __name__ == '__main__':
    # Inicia a aplicação no modo de desenvolvimento, usando o arquivo antigreenwashing.db
    app_instance = create_app('development')
    app_instance.run(debug=True)