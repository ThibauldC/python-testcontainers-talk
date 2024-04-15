from unittest.mock import patch, Mock

import psycopg
import pytest
from testcontainers.postgres import PostgresContainer

from models import Book
from src.db import get_all_books, insert_book


@pytest.fixture(scope="module")
def postgres_connection():
    with PostgresContainer("postgres:13-bookworm") as postgres:
        yield postgres.get_connection_url().replace("+psycopg2", "")


@pytest.fixture
def rerouted_cursor(postgres_connection):
    with psycopg.connect(postgres_connection) as conn:
        with conn.cursor() as cur:
            yield cur
        print("closed")


@pytest.fixture
def book_table(rerouted_cursor):
    with open("tests/sql/test_records.sql") as f:
        sql = f.read()
    rerouted_cursor.execute(sql)
    yield ""
    rerouted_cursor.execute("DROP TABLE book")


def test_get_all_books_with_mocking():
    mock_cur = Mock()
    with patch("src.db.get_cur") as mock_get_cur:
        mock_get_cur.return_value = mock_cur
        mock_cur.fetchall.return_value = [(1, "test", 8), (2, "test2", 2)]
        books = get_all_books()
        assert len(books) == 2


def test_insert_book(postgres_connection, book_table, rerouted_cursor):
    test_book = Book(4, "Fundamentals of Data Engineering", 10)
    with patch('src.db.get_cur') as mock_get_cur:
        mock_get_cur.return_value = rerouted_cursor
        insert_book(test_book)
        rerouted_cursor.execute("SELECT * FROM book")
        books = rerouted_cursor.fetchall()
    assert len(books) == 4


def test_get_all_books(book_table, rerouted_cursor):
    with patch('src.db.get_cur') as mock_get_cur:
        mock_get_cur.return_value = rerouted_cursor
        books = get_all_books()
    assert len(books) == 3
