# Rotas Open Food Facts API

# 2 - endpoint to get product details by name from OFF API
@app.route('/off/search/<product_name>')
def search_off_product(product_name):
    """Busca produto na API Open Food Facts por nome"""
    logger.debug(f"Buscando '{product_name}' na OFF API")
    
    try:
        params = {
            'search_terms': product_name,
            'search_simple': 1,
            'action': 'process',
            'json': 1
        }
        response = requests.get(OFF_API_SEARCH, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        logger.debug(f"OFF API retornou {data.get('count', 0)} resultados")
        return jsonify(data), 200
        
    except requests.exceptions.Timeout:
        error_msg = "Timeout ao consultar Open Food Facts"
        logger.error(error_msg)
        return {"message": error_msg}, 504
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro ao consultar OFF API: {str(e)}"
        logger.error(error_msg)
        return {"message": error_msg}, 502