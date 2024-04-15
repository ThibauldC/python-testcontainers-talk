import unittest
from unittest.mock import patch

import psycopg
from testcontainers.postgres import PostgresContainer

from src.models import Book
from src.db import get_all_books, insert_book


class BookTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgres_container = PostgresContainer("postgres:13-bookworm")
        cls.postgres_container.start()

    def setUp(self):
        self.conn = psycopg.connect(self.postgres_container.get_connection_url().replace("+psycopg2", ""))
        self.cur = self.conn.cursor()
        with open("tests/sql/test_records.sql") as f:
            sql = f.read()
        self.cur.execute(sql)

    def test_insert_book(self):
        test_book = Book(4, "Fundamentals of Data Engineering", 10)
        with patch('src.db.get_cur') as mock_get_cur:
            mock_get_cur.return_value = self.cur
            insert_book(test_book)
        self.cur.execute("SELECT * FROM book")
        books = self.cur.fetchall()
        self.assertEqual(len(books), 4)

    def test_get_all_books(self):
        with patch('src.db.get_cur') as mock_get_cur:
            mock_get_cur.return_value = self.cur
            books = get_all_books()
        self.assertEqual(len(books), 3)

    def tearDown(self):
        self.cur.execute("DROP TABLE book")
        self.cur.close()
        self.conn.close()

    @classmethod
    def tearDownClass(cls):
        cls.postgres_container.stop()
