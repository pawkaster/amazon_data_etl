import csv
import pandas as pd
import urllib.parse
from flask import Flask, jsonify

from src.amazon_scraper import parse_listing
from src.data_processor import preprocess_data

from db import operations as ops
from db.models import Page

app = Flask(__name__)

@app.route('/pages/<query_text>/')
@app.route('/pages/<query_text>/<query_size>')
def pages(query_text, query_size=2):
    data = []
    search_url = "https://www.amazon.de/s?k="
    query_size = 2
    query_text = urllib.parse.quote_plus(query_text)
    search_url += query_text
    pages = []

    new_query = ops.find_query_by_text(query_text)
    if new_query:
        pages = ops.find_pages_by_query_text(
            query_text=query_text
        )
    else:
        # Run scraper for new query
        new_query = ops.create_query(text=query_text)
        data = parse_listing(listing_url=search_url, query_size=query_size)
        df = pd.DataFrame(data)
        df = preprocess_data(df)
        df.to_csv('data/query_results.csv', index=False)
        # Update DB with new pages for this query
        with open('data/query_results.csv', encoding='utf-8', newline='') as file:
            csvreader = csv.DictReader(file, quotechar='"')

            for row in csvreader:
                ops.create_page(**row, query=new_query)
            pages = ops.find_pages_by_query_text(query_text=query_text)
    
    return jsonify(pages)

if __name__ == '__main__':
    app.run()