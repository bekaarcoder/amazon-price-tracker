import requests
import lxml
from bs4 import BeautifulSoup


def get_url_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Accept-Language": "en",
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    name = soup.select_one("#productTitle").get_text().strip()

    price = soup.select_one("#priceblock_dealprice")
    if price is None:
        price = soup.select_one("#priceblock_ourprice")
    price = price.get_text().strip()
    price = float(price[2:].replace(",", ""))

    in_stock = soup.select_one("#availability > span").get_text().strip()

    return name, price, in_stock