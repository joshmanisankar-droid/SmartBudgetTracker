import requests
from bs4 import BeautifulSoup
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}
def scrape_books(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception("Failed to fetch webpage")
    soup = BeautifulSoup(response.text, "lxml")
    title = soup.find("h1").get_text(strip=True)
    price_text = soup.find("p", class_="price_color").get_text(strip=True)
    price = float(
        price_text
        .replace("Â", "")
        .replace("£", "")
        .strip()
    )
    image = soup.find("img")["src"]
    image = image.replace("../../", "https://books.toscrape.com/")
    availability = soup.find(
        "p",
        class_="instock availability"
    ).get_text(strip=True)
    return {
        "title": title,
        "price": price,
        "image": image,
        "availability": availability,
        "website": "BooksToScrape"
    }