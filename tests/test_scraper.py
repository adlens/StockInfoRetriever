import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scraper import find_urls, get_stock_info

# A list of test cases, each case is a tuple (html_file_name, expected_urls)
search_page_data = [
    ("test_search_page_at.html", ['https://www.hl.co.uk/shares/shares-search-results/B11V7W9', 'https://www.hl.co.uk/shares/shares-search-results/BNG2M15', 'https://www.hl.co.uk/shares/shares-search-results/BMVQDZ6', 'https://www.hl.co.uk/shares/shares-search-results/0435594', 'https://www.hl.co.uk/shares/shares-search-results/0871079', 'https://www.hl.co.uk/shares/shares-search-results/BM9CMX7', 'https://www.hl.co.uk/shares/shares-search-results/BD95V14', 'https://www.hl.co.uk/shares/shares-search-results/BLH4250', 'https://www.hl.co.uk/shares/shares-search-results/BYZTVM8', 'https://www.hl.co.uk/shares/shares-search-results/BKS7ZV8', 'https://www.hl.co.uk/shares/shares-search-results/0060929', 'https://www.hl.co.uk/shares/shares-search-results/BP4BSM1', 'https://www.hl.co.uk/shares/shares-search-results/BKQVBN6', 'https://www.hl.co.uk/shares/shares-search-results/BLFH013', 'https://www.hl.co.uk/shares/shares-search-results/BLBNS44', 'https://www.hl.co.uk/shares/shares-search-results/BZ12TX5', 'https://www.hl.co.uk/shares/shares-search-results/2938002', 'https://www.hl.co.uk/shares/shares-search-results/B03HFD5', 'https://www.hl.co.uk/shares/shares-search-results/BD60BG7', 'https://www.hl.co.uk/shares/shares-search-results/BP488W2', 'https://www.hl.co.uk/shares/shares-search-results/5608915', 'https://www.hl.co.uk/shares/shares-search-results/BMTWBP2', 'https://www.hl.co.uk/shares/shares-search-results/BDRY7P9', 'https://www.hl.co.uk/shares/shares-search-results/B00MZ00', 'https://www.hl.co.uk/shares/shares-search-results/BJVNMJ3', 'https://www.hl.co.uk/shares/shares-search-results/2045247', 'https://www.hl.co.uk/shares/shares-search-results/BF0CK44', 'https://www.hl.co.uk/shares/shares-search-results/BMYRFN8', 'https://www.hl.co.uk/shares/shares-search-results/2060518', 'https://www.hl.co.uk/shares/shares-search-results/B2RK5K1', 'https://www.hl.co.uk/shares/shares-search-results/BN6M8F1', 'https://www.hl.co.uk/shares/shares-search-results/BP4WT09', 'https://www.hl.co.uk/shares/shares-search-results/B12TR11', 'https://www.hl.co.uk/shares/shares-search-results/BMXS6G2', 'https://www.hl.co.uk/shares/shares-search-results/BN4Q5K9', 'https://www.hl.co.uk/shares/shares-search-results/BMTVQR6', 'https://www.hl.co.uk/shares/shares-search-results/2526117', 'https://www.hl.co.uk/shares/shares-search-results/BRDYC56', 'https://www.hl.co.uk/shares/shares-search-results/BMZL8K7', 'https://www.hl.co.uk/shares/shares-search-results/BDHF495', 'https://www.hl.co.uk/shares/shares-search-results/B9B9F36', 'https://www.hl.co.uk/shares/shares-search-results/BLDBN41', 'https://www.hl.co.uk/shares/shares-search-results/BLDBN52', 'https://www.hl.co.uk/shares/shares-search-results/BMD4B09', 'https://www.hl.co.uk/shares/shares-search-results/2315359', 'https://www.hl.co.uk/shares/shares-search-results/BD0NG78', 'https://www.hl.co.uk/shares/shares-search-results/5654781', 'https://www.hl.co.uk/shares/shares-search-results/BFXZQW0', 'https://www.hl.co.uk/shares/shares-search-results/B0C8KV2', 'https://www.hl.co.uk/shares/shares-search-results/BP8JT73', 'https://www.hl.co.uk/shares/search-for-investments?stock_search_input=at&offset=50']
),
    ("test_search_page_baaaaa.html", [])
]

@pytest.mark.parametrize("html_file_name, expected_urls", search_page_data)
def test_find_urls(html_file_name, expected_urls):
    # Read stored HTML file
    html_file_path = Path(__file__).parent / html_file_name
    with open(html_file_path, "r") as file:
        html_content = file.read()

    # Create a mock response object
    mock_response = Mock()
    mock_response.text = html_content 

    # Call find_urls with mock response object
    urls = find_urls(mock_response)
    # Assert that the extracted urls match the expected values
    assert urls == expected_urls, "find_urls did not return the expected URLs"



stock_info_page_data = [
    ("test_stock_info_page_sain.html", {"name": "Scottish American Investment Co plc (SAIN) Ordinary 25p Shares", "info": {'Open': '498.00p', 'Trade high': '498.72p', 'Year high': '543.00p', 'Estimated NAV': '554.56', 'Previous close': '497.50p', 'Trade low': '494.83p', 'Year low': '450.00p', 'Premium/Discount': '-9.66%', 'Volume': '170,324', 'Dividend yield': '2.84%', 'Currency': 'GBX'}}),
    ("test_stock_info_page_amat.html", {"name": "Amati Aim VCT plc (AMAT) Ordinary 5p", "info": {'Open': '86.50p', 'Trade high': '86.00p', 'Year high': '117.00p', 'Estimated NAV': '92.91', 'Previous close': '86.50p', 'Trade low': '86.00p', 'Year low': '86.00p', 'Premium/Discount': '-6.90%', 'Volume': '3,257', 'Dividend yield': '5.78%', 'Currency': 'GBX'}}),
]

@pytest.mark.parametrize("html_file_name, expected_info", stock_info_page_data)
def test_get_stock_info(html_file_name, expected_info):
    # Read stored HTML file for stock information
    html_file_path = Path(__file__).parent / html_file_name
    with open(html_file_path, "r") as file:
        html_content = file.read()

    # Create a mock response object with HTML content
    mock_response = Mock()
    mock_response.text = html_content

    # Call get_stock_info with mock response object
    stock_name, stock_info = get_stock_info(mock_response)
    print(stock_name, stock_info)
    # Assert that the extracted stock name and info match the expected values
    assert stock_name == expected_info['name'], f"Expected stock name '{expected_info['name']}', but got '{stock_name}'"
    assert stock_info == expected_info['info'], f"Expected stock info {expected_info['info']}, but got {stock_info}"