import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

def find_urls(search_input):
    search_url = "https://www.hl.co.uk/shares/search-for-investments?stock_search_input=" + search_input
    response = requests.get(search_url)
    urls = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_list = soup.find('tbody', id="stock_list_tbody")
        stocks = stock_list.find_all('tr')
        for stock in stocks:
            tds = stock.find_all('td')
            try:
                link = tds[1].find('a')['href']
                urls.append(link)
            except:
                continue
    return urls

def get_stock_info(stock_url):
    response = requests.get(stock_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and clean stock name
        stock_name = soup.find('h1').text.strip()
        cleaned_name = stock_name.replace('\r', ' ').replace('\n', ' ')
        final_name = ' '.join(cleaned_name.split())

        # Store all stock related info in a dictionary
        security_info = {}

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
def api_get_stock_info(search_input):
    if not search_input:
        return jsonify({'error': 'Missing epic name'}), 400
    try:
        results = {}
        urls = find_urls(search_input)
        for url in urls:
            stock_name, stock_info = get_stock_info(url)
            results[stock_name] = stock_info
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)