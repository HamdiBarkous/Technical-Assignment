from requests_html import HTMLSession
import sqlite3

class Scraper():
    def scrape_books(self, category, min_price=None, max_price=None, rating=None):
        # Mapping of book categories to their respective IDs on the website
        cat = {'travel': 2, 'mystery': 3, 'historical Fiction': 4, 'sequential Art': 5,
               'classics': 6, 'philosophy': 7, 'romance': 8, 'womens Fiction': 9,
               'fiction': 10, 'childrens': 11, 'religion': 12, 'nonfiction': 13, 'music': 14}

        # Constructs URL for the specified category
        url = f'https://books.toscrape.com/catalogue/category/books/{category}_{cat[category]}/index.html'

        s = HTMLSession()
        r = s.get(url)
        r.raise_for_status()

        # Connects to a SQLite database and creates a table if it doesn't exist
        with sqlite3.connect('books.db') as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS books
                         (title TEXT, price REAL, availability TEXT, rating TEXT)''')

            article_list = []
            articles = r.html.find('article.product_pod')

            for book in articles:
                # Extracts relevant data from each book article
                price = book.find('p.price_color', first=True).text.strip().lstrip('£')
                availability = book.find('p.instock.availability', first=True).text.strip()
                rating_class = book.find('p.star-rating', first=True).attrs['class']
                book_rating = rating_class[1]
                title = book.find('h3 a', first=True).attrs['title']

                # Filters based on the price and rating criteria, if provided
                if min_price and float(price) < float(min_price):
                    continue
                if max_price and float(price) > float(max_price):
                    continue
                if rating and book_rating != rating:
                    continue

                book_info = {
                    'Title': title,
                    'Price': f"£{price}",
                    'Availability': availability,
                    'Rating': book_rating
                }
                article_list.append(book_info)

                # Inserts book data into the SQLite database
                c.execute("INSERT INTO books VALUES (?, ?, ?, ?)", tuple(book_info.values()))

            return article_list

    def get_book_prices(self, category):
        # Similar to the above method, but retrieves only prices
        cat = cat = {'travel': 2, 'mystery': 3, 'historical Fiction': 4, 'sequential Art': 5,
               'classics': 6, 'philosophy': 7, 'romance': 8, 'womens Fiction': 9,
               'fiction': 10, 'childrens': 11, 'religion': 12, 'nonfiction': 13, 'music': 14}

        url = f'https://books.toscrape.com/catalogue/category/books/{category}_{cat[category]}/index.html'

        s = HTMLSession()
        r = s.get(url)
        r.raise_for_status()

        prices = []
        articles = r.html.find('article.product_pod')

        for book in articles:
            price = book.find('p.price_color', first=True).text.strip().lstrip('£')
            prices.append(float(price))

        return prices


