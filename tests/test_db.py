from unittest.mock import patch

import psycopg
import pytest
from testcontainers.postgres import PostgresContainer

from src.db import get_all_books


@pytest.fixture
def postgres_connection():
    with PostgresContainer("postgres:13-bookworm") as postgres:
        yield postgres.get_connection_url().replace("+psycopg2", "")


@pytest.fixture
def rerouted_cursor(postgres_connection):
    with psycopg.connect(postgres_connection) as conn:
        with conn.cursor() as cur:
            yield cur


@pytest.fixture
def book_table(postgres_connection):
    with psycopg.connect(postgres_connection) as conn:
        with conn.cursor() as cur:
            with open("tests/sql/test_records.sql") as f:
                sql = f.read()
            cur.execute(sql)
    yield ""


def test_get_all_books(book_table, rerouted_cursor):
    with patch('src.db.get_cur') as mock_get_cur:
        mock_get_cur.return_value = rerouted_cursor
        books = get_all_books()
        assert len(books) == 3
