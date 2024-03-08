import logging
import os
from flask import Flask, request, jsonify, url_for
from flask_caching import Cache
from scraper import find_urls, get_stock_info, load_search_results

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)
cache.init_app(app)

logging.basicConfig(level=logging.INFO)

search_results_file = 'search_results.json'
search_results = load_search_results(search_results_file)

@app.route('/get_stock_info/<search_input>', methods=['GET'])
@cache.memoize(timeout=50)
def api_get_stock_info(search_input):
    if not search_input:
        return jsonify({'error': 'Missing search input'}), 400
    try:
        results = {}
        base_url = os.getenv("BASE_URL", "https://www.hl.co.uk/shares/search-for-investments")
        urls = find_urls(search_input.lower(), base_url, search_results, search_results_file)
        for url in urls:
            stock_name, stock_info = get_stock_info(url)
            if stock_name:
                results[stock_name] = stock_info
        return jsonify(results), 200
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
