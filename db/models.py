from typing import List
from sqlalchemy import String, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Query(Base):
    __tablename__ = "query"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)

    pages: Mapped[List["Page"]] = relationship(
        back_populates="query", cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"Query(id={self.id}, text={self.text})"

class Page(Base):
    __tablename__ = "page"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    rating: Mapped[float]
    currency: Mapped[str] = mapped_column(String(5))
    price: Mapped[float]
    img_src: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)
    query_id: Mapped[int] = mapped_column(ForeignKey("query.id"))

    query: Mapped["Query"] = relationship(back_populates="pages")
