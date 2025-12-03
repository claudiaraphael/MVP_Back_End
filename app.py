from flask_openapi3 import OpenAPI
from model import Session, Product

from schemas import ProductSchema, ProductViewSchema, ErrorSchema
from logger import logger

# TO DO:
# - separate responsibilities in this file into different files: run.py, __init__.py, OFF endpoints, CRUD endpoints


# import ennvironment variables

app = Flask(__name__)



# Read Routes
# 1 - endpoint to check if the server is running
@app.route('/')
def home():
    return "Welcome!"

# 2 - Endpoint para pegar o produto da base de dados da OFF
@app.get('/product', tags=[product_tag],
         responses={"200": ProductViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoSearchSchema):
    
    """Search for a product in the local data base"""
    product_name = query.name
    logger.debug(f"Searching product locally: '{product_name}'")
    
    session = Session()
    try:
        product = session.query(Product).filter(
            Product.name == product_name
        ).first()
        
        if not product:
            error_msg = "Product not found."
            logger.warning(f"'{product_name}' not found")
            return {"message": error_msg}, 404
        
        logger.debug(f"Product found: '{product.name}'")
        return product, 200
        
    finally:
        session.close()  # ✅ IMPORTANTE: sempre fechar session


# adicionar o endpoint de adicionar produto (C DO CRUD)

@app.post('/add_product', tags=[product_tag],
        responses={"200": ProductViewSchema, "409": ErrorSchema, "400": ErrorSchema}  )
def add_product(form: ProductSchema):
    """ Adds a new product to the data base """
    product = Product(
        name=form.name,
        barcode=form.barcode
    )
    logger.debug(f"Adding a product: '{product}'")

    try:
        session = Session()
        session.add(product)
        session.commit()
        logger.debug(f"Product added successfully: '{product.name}'")
        return product, 200
    
    except IntegrityError as e:
        error_msg = "Product is alredy in the data base"
        logger.warning(f"Error adding '{product.name}': {error_msg}")
        return {"message": error_msg}, 409
    
    except Exception as e:
        error_msg = "Could not add the product"
        logger.warning(f"Erro: {error_msg}")
        return {"message": error_msg}, 400



# 3 - endpoint to get product details by barcode

# 4 - endpoint to get product history (placeholder)
@app.get('/api/products_history')
def get_products_history():
    # Placeholder for product history retrieval logic
    return jsonify({"message": "Product history endpoint"})

@app.delete('/produto', tags=[product_tag],
            responses={"200": ProductDelSchema, "404": ErrorSchema})
def del_produto(query: ProductBuscaSchema):
    """Deleta produto por nome"""
    product_name = unquote(unquote(query.name))
    logger.debug(f"Deletando produto: '{product_name}'")
    
    session = Session()
    try:
        count = session.query(Product).filter(
            Product.name == product_name
        ).delete()
        session.commit()
        
        if count:
            logger.debug(f"Product '{product_name}' deleted")
            return {"message": "Producto removed", "name": product_name}, 200
        else:
            error_msg = "Produto não encontrado"
            logger.warning(f"'{product_name}' não encontrado para deletar")
            return {"message": error_msg}, 404
            
    finally:
        session.close()


# Run the Flask app
# the if statement with __name == '__main__' means that this code block will only be executed if the script is run directly (not imported as a module in another script).
if __name__ == '__main__':
    app.run(debug=True)


# usar o codigo da API do professor como exemplo pra add produtos à base


# Open Food Facts API
# criar codigo para consulta de dados na base de dados da API e outro pra Open Food Facts API.
# https://openfoodfacts.github.io/openfoodfacts-server/api/ - documentacao do OFF API







# If you submit the product's nutritional values and category, you'll get the Nutri-Score.
# If you submit the product ingredients, you'll get the NOVA group (about food ultra-processing), additives, allergens, normalized ingredients, vegan, vegetarian…
# If you submit the product's category and labels, you'll get the Eco-Score (a rating of the product's environmental impact)




# Referências

# A API da Open Food Facts opera com base na Open Database License: https://opendatacommons.org/licenses/odbl/1-0/
# The individual contents of the database are available under the Database Contents License(https://opendatacommons.org/licenses/dbcl/1-0/).
# Product images are available under the Creative Commons Attribution ShareAlike license (https://creativecommons.org/licenses/by-sa/3.0/deed.en). They may contain graphical elements subject to copyright or other rights that may, in some cases, be reproduced (quotation rights or fair use).

