import pytest
from src.models import Book

@pytest.fixture(autouse=True)
def reset_book_ids():
    Book._last_id = 0
    yield
    Book._last_id = 0