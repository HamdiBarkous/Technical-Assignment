from scraper import Scraper
from fastapi import FastAPI, Query
from matplotlib import pyplot as plt
import io
from starlette.responses import StreamingResponse
import numpy as np
import seaborn as sns

app = FastAPI()
books = Scraper()
#print(books.get_book_prices('travel'))
#print(books.scrape_books('travel'))

@app.get('/{cat}')
async def read_item(cat, min_price: float = Query(None), max_price: float = Query(None), rating: str = Query(None)):
    return books.scrape_books(cat, min_price, max_price, rating)


@app.get("/histogram/{category}")
async def histogram(category: str):
    prices = books.get_book_prices(category)

    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")  # Set the style of the visualization
    sns.histplot(prices, bins=20, kde=True, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title(f'Price Distribution of {category.capitalize()} Books', fontsize=15, fontweight='bold')
    plt.xlabel('Price (£)', fontsize=12)
    plt.ylabel('Number of Books', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, which='major', linestyle='--', linewidth='0.5', color='grey')  # Add gridlines

    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300)  # Save with high dpi for better resolution
    img.seek(0)
    plt.close()

    return StreamingResponse(img, media_type="image/png")