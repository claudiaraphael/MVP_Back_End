from distro import name
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OFF_BASE = 'https://world.openfoodfacts.net'
# fetch products by name
OFF_API_PRODUCT = OFF_BASE + '/cgi/search.pl?search_terms={name}&search_simple=1&action=process&json=1'
# or try
OFF_API_PRODUCT_2 = OFF_BASE + '/cgi/search.pl'
# fetch product by barcode:
OFF_API_BARCODE = OFF_BASE + '/api/v2/product/{barcode}'

# Read Routes
# 1 - endpoint to check if the server is running
@app.route('/')
def home():
    return "Welcome!"

# adicionar o endpoint de adicionar produto (C DO CRUD)
def add_produto():
    session = Session()
    produto = Produto(
        nome=request.form.get("nome"),
        quantidade=request.form.get("quantidade"),
        valor=request.form.get("valor")
    )
    try:
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return jsonify(produto.__dict__), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

# @app.route('/add_product', methods=['POST'])

# 2 - endpoint to get product details by name from OFF API
@app.route('/api/product/<name>')
def get_product(name):
    response = requests.get(OFF_API_PRODUCT.format(name=name))
    return jsonify(response.json())

@app.route('/get_produto/<produto_id>', methods=['GET'])
def get_product_from_mvp_api(produto_id):
    session = Session()
    produto = session.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        error_msg = "Produto não encontrado na base :/"
        return jsonify({"error": error_msg}), 404
    else:
        return jsonify(produto.__dict__), 200


# 3 - endpoint to get product details by barcode
@app.route('/api/barcode/<barcode>')
def get_product_by_barcode(barcode):
    response = requests.get(OFF_API_BARCODE.format(barcode=barcode))
    return jsonify(response.json())

# 4 - endpoint to get product history (placeholder)
@app.route('/api/products_history')
def get_products_history():
    # Placeholder for product history retrieval logic
    return jsonify({"message": "Product history endpoint"})

@app.route('/del_produto/<produto_id>', methods=['DELETE'])
def del_produto(produto_id):
    session = Session()
    count = session.query(Produto).filter(Produto.id == produto_id).delete()
    session.commit()
    if count ==1:
        return jsonify({"message": f"Produto {produto_id} deletado com sucesso."}), 200
    else: 
        error_msg = "Produto não encontrado na base :/"
        return jsonify({"error": error_msg}), 404




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

