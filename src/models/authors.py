from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from application.database import Base


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    lastname = Column(String(50))

    books = relationship('Book', back_populates='author')
