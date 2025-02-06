import pandas as pd
from amazon_scraper import parse_listing
import urllib.parse

def main():
    data = []
    search_url = "https://www.amazon.de/s?k="
    query = "gaming keyboard"
    query = urllib.parse.quote_plus(query)
    search_url += query
    data = parse_listing(listing_url=search_url, query_size=5)
    df = pd.DataFrame(data)
    df.to_csv('data/query_results.csv', index=False)

if __name__ == '__main__':
    main()