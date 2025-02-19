from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
          (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

visited_urls = set()

def get_product_info(url):
    """
    Scrape product information from the provided url: title, rating, price, 
    image
    :param url: URL string of the product
    :return dictionary with product information
    """

    response = requests.get(url=url, headers=custom_headers)
    soup = BeautifulSoup(response.text, 'lxml')
    product_info = {}
    try:
        title_element = soup.select_one('#productTitle')
        product_info['title'] = title_element.text.strip()

        rating_element = soup.select_one('#acrPopover > span > a > \
                                        span.a-size-base')
        product_info['rating'] = rating_element.text.strip().replace(',', '.')

        price_element = soup.select_one('span.a-offscreen')
        product_info['price'] = price_element.text

        image_element = soup.select_one('#landingImage')
        product_info['img_src'] = image_element.attrs.get('src')

        product_info['url'] = url
    except Exception as e:
        print(e)
        product_info = {}

    return product_info

def parse_listing(listing_url, query_size=10):
    """
    Creates list of products information from the scraped data
    :param listing_url: URL string of the listing
    :param query_size: Number of pages to scrap. Default 10.
    :return list of product information
    """

    global visited_urls
    response = requests.get(url=listing_url, headers=custom_headers)
    print(response.status_code)
    soup_listing = BeautifulSoup(response.text, 'lxml')
    link_elements = soup_listing.select('[data-cy=title-recipe] > \
                                        a.a-link-normal')
    page_data = []

    for link in link_elements:
        full_url = urljoin(listing_url, link.attrs.get('href'))
        if full_url not in visited_urls:
            visited_urls.add(full_url)
            print(f"Scrapping product from {full_url[:100]}", flush=True)
            product_info = get_product_info(full_url)
            if product_info:
                page_data.append(product_info)

            if len(page_data) >= query_size:
                return page_data

    next_page_element = soup_listing.select_one('a.s-pagination-next')
    if next_page_element:
        next_page_url = next_page_element.attrs.get('href')
        next_page_url = urljoin(listing_url, next_page_url)
        print(f"Scrapping next page: {next_page_url}", flush=True)
        remaining_query_size = query_size - len(page_data)
        page_data += parse_listing(next_page_url, remaining_query_size)
    
    return page_data






