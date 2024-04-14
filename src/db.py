from contextlib import contextmanager

from psycopg.cursor import Cursor
from src.models import Book


@contextmanager
def get_cur() -> Cursor:
    pass


def get_all_books() -> list[Book]:
    with get_cur() as cur:
        cur.execute("SELECT * FROM book")
        book_tups = cur.fetchall()
    books = [Book(*book_tup) for book_tup in book_tups]
    return books



# function to SELECT *

# SELECT * WHERE book rating > 8/10

# test where

# test where you verify the input rating (0 <= x <= 10)

# test where you change the input