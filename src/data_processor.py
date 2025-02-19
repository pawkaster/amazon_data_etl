import re

def preprocess_data(data_frame):
    """
    Drops rows with empty prices and splits price into separate price and 
    currency columns. Fixes columns dtypes.
    :param data_frame: data frame for processing
    :return Processed data frame
    """
    # Drop rows with incorrect price
    price_pattern = "€[0-9]{1,5}\\.[0-9]{2}"
    data_frame = data_frame[data_frame['price'].str.contains(price_pattern, na=False)]

    # Create separate column for price and currency
    data_frame.insert(data_frame.columns.get_loc('price'), 'currency', 
                      data_frame['price'].str[:1])
    data_frame['price'] = data_frame['price'].str[1:]

    # Fix column dtypes
    convert_dict = {
        'title': str,
        'rating': float,
        'currency': str,
        'price': float,
        'img_src': str,
        'url': str,
    }

    data_frame = data_frame.astype(convert_dict)

    return data_frame