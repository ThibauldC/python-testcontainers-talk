from contextlib import contextmanager

from psycopg.cursor import Cursor
from src.models import Book


def get_cur() -> Cursor:
    pass


def get_all_books() -> list[Book]:
    cur = get_cur()
    cur.execute("SELECT * FROM book")
    book_tups = cur.fetchall()
    books = [Book(*book_tup) for book_tup in book_tups]
    return books


def insert_book(book: Book) -> None:
    cur = get_cur()
    cur.execute("INSERT INTO book(id, title, rating) VALUES(%s, %s, %s)", (book.id, book.title, book.rating))
    cur.connection.commit()



# function to SELECT *

# SELECT * WHERE book rating > 8/10

# test where

# test where you verify the input rating (0 <= x <= 10)

# test where you change the input