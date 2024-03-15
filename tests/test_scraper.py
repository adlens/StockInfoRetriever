import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scraper import find_urls

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
    # print(html_file_name, urls)
    assert urls == expected_urls, "find_urls did not return the expected URLs"
