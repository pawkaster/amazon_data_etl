import pandas as pd
import urllib.parse

from amazon_scraper import parse_listing
from data_processor import preprocess_data

def main():
    data = []
    search_url = "https://www.amazon.de/s?k="
    query = "gaming keyboard"
    query = urllib.parse.quote_plus(query)
    search_url += query
    data = parse_listing(listing_url=search_url, query_size=10)
    df = pd.DataFrame(data)
    df = preprocess_data(df)
    df.to_csv('data/query_results.csv', index=False)

if __name__ == '__main__':
    main()