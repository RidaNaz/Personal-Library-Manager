from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

# SQLite database
DATABASE_URL = "sqlite:///library.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Book model
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String)
    added_on = Column(Date, default=date.today)

# Create tables
Base.metadata.create_all(engine)

# CRUD functions
def add_book(title, author, genre):
    book = Book(title=title, author=author, genre=genre)
    session.add(book)
    session.commit()

def get_all_books():
    return session.query(Book).all()

def delete_book(book_id):
    book = session.query(Book).filter_by(id=book_id).first()
    if book:
        session.delete(book)
        session.commit()
