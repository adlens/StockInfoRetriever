from flask import Flask, jsonify
from scraper import find_urls, get_stock_info, load_search_results, safe_request
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import os
from flask_caching import Cache

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'  # Default Redis connection URL
cache = Cache(app)
cache.init_app(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})

logging.basicConfig(level=logging.INFO)

search_results_file = 'search_results.json'
search_results = load_search_results(search_results_file)

@app.route('/get_stock_info/<search_input>', methods=['GET'])
@cache.memoize(timeout=300)
def api_get_stock_info(search_input):
    if not search_input:
        logging.error("Missing search input")
        return jsonify({'error': 'Missing search input'}), 400
    try:
        base_url = os.getenv("BASE_URL", "https://www.hl.co.uk/shares/search-for-investments")
        urls = find_urls(search_input.lower(), base_url, search_results, search_results_file)
        
        results = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_response = {executor.submit(safe_request, url): url for url in urls}
            for future in as_completed(future_to_response):
                try:
                    response = future.result()
                    if response:
                        stock_name, stock_info = get_stock_info(response)
                        if stock_name:
                            results[stock_name] = stock_info
                except Exception as exc:
                    logging.error(f'An exception is generated: {exc}')
        
        return jsonify(results), 200
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
