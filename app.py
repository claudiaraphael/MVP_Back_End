from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OFF_API_PRODUCT = 'https://world.openfoodfacts.net/cgi/search.pl?search_terms={name}&search_simple=1&action=process&json=1'
OFF_API_BARCODE = 'https://world.openfoodfacts.net/api/v2/product/{barcode}'

# usar o codigo da API do professor como exemplo pra add produtos à base
# criar um analogo para consulta de dados na base de dados da API e outro pra Open Food Facts API.
# https://openfoodfacts.github.io/openfoodfacts-server/api/ - documentacao do OFF API

@app.route('/api/search')
def search_products():
    query = request.args.get('q', '')
    params = {
        'search_terms': query,
        'search_simple': 1,
        'action': 'process',
        'json': 1,
    }
    resp = requests.get(OFF_API_PRODUCT, params=params)
    return jsonify(resp.json())


@app.route('/api/barcode/<barcode>')
def get_product_by_barcode(barcode):
    resp = requests.get(OFF_API_BARCODE.format(barcode))
    return jsonify(resp.json())


# the if statement with __name == '__main__' means that this code block will only be executed if the script is run directly (not imported as a module in another script).
if __name__ == '__main__':
    app.run(debug=True)

# always use a custom User-Agent to identify your app (to not risk being identified as a bot). The User-Agent should be in the form of AppName/Version (ContactEmail). For example, MyApp/1.0 (myapp@example.com).
# Create an account on the Open Food Facts app for your app and fill out the API usage form so that we can identify your usage and prevent potential bans. From there, you have two options:
# The preferred one: Use the login API to get a session cookie and use this cookie for authentication in your subsequent requests. However, the session must always be used from the same IP address, and there's a limit on sessions per user (currently 10) with older sessions being automatically logged out to stay within the limit.






























# If you submit the product's nutritional values and category, you'll get the Nutri-Score.
# If you submit the product ingredients, you'll get the NOVA group (about food ultra-processing), additives, allergens, normalized ingredients, vegan, vegetarian…
# If you submit the product's category and labels, you'll get the Eco-Score (a rating of the product's environmental impact)




# Referências

# A API da Open Food Facts opera com base na Open Database License: https://opendatacommons.org/licenses/odbl/1-0/
# The individual contents of the database are available under the Database Contents License(https://opendatacommons.org/licenses/dbcl/1-0/).
# Product images are available under the Creative Commons Attribution ShareAlike license (https://creativecommons.org/licenses/by-sa/3.0/deed.en). They may contain graphical elements subject to copyright or other rights that may, in some cases, be reproduced (quotation rights or fair use).

