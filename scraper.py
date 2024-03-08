import os
import requests
import json
from bs4 import BeautifulSoup
import logging

session = requests.Session()

def safe_request(url):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def load_search_results(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_search_results(file_path, search_results):
    with open(file_path, 'w') as file:
        json.dump(search_results, file)

def update_search_results(search_input, urls, search_results, file_path):
    dict_size = 100
    if search_input in search_results:
        search_results[search_input]['urls'] = urls
        search_results[search_input]['count'] += 1
    else:
        search_results[search_input] = {'urls': urls, 'count': 1}

    if len(search_results) > dict_size:
        least_used = min(search_results.keys(), key=lambda k: search_results[k]['count'])
        del search_results[least_used]
    save_search_results(file_path, search_results)

def find_urls(search_input, base_url, search_results, file_path):
    if search_input in search_results:
        search_results[search_input]['count'] += 1
        save_search_results(file_path, search_results)
        return search_results[search_input]['urls']
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
        update_search_results(search_input, urls, search_results, file_path)
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
