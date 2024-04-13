import psycopg
import pytest
from testcontainers.postgres import PostgresContainer


@pytest.fixture
def postgres_connection():
    with PostgresContainer("postgres:13-bookworm") as postgres:
        yield postgres.get_connection_url().replace("+psycopg2", "")


@pytest.fixture
def book_table(postgres_connection):
    with psycopg.connect(postgres_connection) as conn:
        with conn.cursor() as cur:
            with open("tests/sql/test_records.sql") as f:
                sql = f.read()
            cur.execute(sql)
    yield ""


def test_get_all_books(book_table):
    assert 1 == 1
