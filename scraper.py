import os
import logging
import requests
import json
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, url_for
from flask_caching import Cache

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)
cache.init_app(app)

logging.basicConfig(level=logging.INFO)

session = requests.Session()

def safe_request(url):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def load_search_results():
    # Load saved seaching url results from JSON file
    if os.path.exists(search_results_file):
        with open(search_results_file, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_search_results():
    # Update the url results in JSON
    with open(search_results_file, 'w') as file:
        json.dump(search_results, file)


def update_search_results(search_input, urls):
    # Add or update search results and maintain size limit
    global search_results
    dict_size = 100
    # Increment count if exists, else add new entry with count 1
    if search_input in search_results:
        search_results[search_input]['urls'] = urls
        search_results[search_input]['count'] += 1
    else:
        search_results[search_input] = {'urls': urls, 'count': 1}
    
    # Check size and remove the least frequently used if necessary
    
    if len(search_results) > dict_size:
        # Find the search input with the minimum count
        least_used = min(search_results.keys(), key=lambda k: search_results[k]['count'])
        del search_results[least_used]
    save_search_results()


search_results_file = 'search_results.json'
search_results = load_search_results()

def find_urls(search_input):
    global search_results
    # If search_input is already recorded, directly return the results
    if search_input in search_results:  
        search_results[search_input]['count'] += 1  # Update count every time it's accessed
        save_search_results()
        return search_results[search_input]['urls']
    base_url = os.getenv("BASE_URL", "https://www.hl.co.uk/shares/search-for-investments")
    search_url = f"{base_url}?stock_search_input={search_input}"
    response = safe_request(search_url)
    urls = []
    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_list = soup.find('tbody', id="stock_list_tbody")
        if stock_list:
            stocks = stock_list.find_all('tr')
            for stock in stocks:
                link_element = stock.find('td').find('a', href=True)
                if link_element:
                    urls.append(link_element['href'])
    if urls:
        update_search_results(search_input, urls)
    return urls

def get_stock_info(stock_url):
    response = safe_request(stock_url)
    final_name, security_info = "", {}
    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_name = soup.find('h1')
        if stock_name:
            cleaned_name = ' '.join(stock_name.text.strip().split())
            final_name = cleaned_name
            security_details = soup.find("div", id="security-detail")
            nested_divs = security_details.select('div div')
            for div in nested_divs:
                tag = div.find('span')
                if tag:
                    tag_value = tag.text.strip()
                else:
                    continue
                value = div.find('strong')
                if value:
                    value = value.text.strip()
                else:
                    continue
                security_info[tag_value] = value
    return final_name, security_info

@app.route('/get_stock_info/<search_input>', methods=['GET'])
@cache.memoize(timeout=50)
def api_get_stock_info(search_input):
    if not search_input:
        return jsonify({'error': 'Missing search input'}), 400
    try:
        results = {}
        urls = find_urls(search_input.lower())
        for url in urls:
            stock_name, stock_info = get_stock_info(url)
            if stock_name:  # Ensure stock_name is not empty
                results[stock_name] = stock_info
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
