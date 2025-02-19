from sqlalchemy import select
from sqlalchemy.orm import Session

from db.engine import engine
from db.models import Page, Query

def create_query(text):
    with Session(engine) as session:
        query = Query(text=text)
        session.add(query)
        session.commit()
        return query

def find_queries():
    with Session(engine) as session:
        query = select(Query)
        result = session.scalars(query)
        return result.all()
    
def find_query_by_text(text):
    with Session(engine) as session:
        query = select(Query).filter_by(text=text)
        result = session.scalars(query)
        return result.first()

def create_page(title, rating, currency, price, img_src, url, query):
    with Session(engine) as session:
        page = Page(
            title=title,
            rating=rating,
            currency=currency,
            price=price,
            img_src=img_src,
            url=url,
            query=query
        )
        session.add(page)
        session.commit()

def find_pages_by_query_text(query_text):
    with Session(engine) as session:
        current_query = find_query_by_text(query_text)
        query = select(Page).filter_by(query=current_query)\
            .order_by(Page.rating)
        result = session.scalars(query).all()

        result_dict = [
            {
                'title': page.title,
                'rating': page.rating,
                'currency': page.currency,
                'price': page.price,
                'img_src': page.img_src,
                'url': page.url,
            } 
            for page in result
        ]
        return result_dict