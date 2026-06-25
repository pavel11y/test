import pytest
import tempfile
from pathlib import Path
from src.storage import Storage
from src.models import Book

class TestStorage:
    @pytest.fixture(autouse=True)
    def reset_ids(self):
        Book._last_id = 0
        yield
        Book._last_id = 0
    
    @pytest.fixture
    def temp_storage(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test_library.json"
            storage = Storage(str(file_path))
            yield storage
    
    def test_storage_creation(self, temp_storage):
        assert temp_storage.file_path.exists()
        assert temp_storage.file_path.parent.exists()
    
    def test_add_book(self, temp_storage):
        book = Book("Тест", "Тестов", 2020)
        temp_storage.add_book(book)
        
        books = temp_storage.get_all_books()
        assert len(books) == 1
        assert books[0].title == "Тест"
        assert books[0].author == "Тестов"
        assert books[0].year == 2020
        assert books[0].book_id == 1
    
    def test_get_book_by_id(self, temp_storage):
        book = Book("Тест", "Тестов", 2020)
        temp_storage.add_book(book)
        
        retrieved = temp_storage.get_book_by_id(book.book_id)
        assert retrieved is not None
        assert retrieved.book_id == book.book_id
        assert retrieved.title == book.title
    
    def test_get_book_by_id_not_found(self, temp_storage):
        retrieved = temp_storage.get_book_by_id(999)
        assert retrieved is None
    
    def test_update_book(self, temp_storage):
        book = Book("Тест", "Тестов", 2020)
        temp_storage.add_book(book)
        
        book.title = "Новое название"
        book.update_status("прочитано")
        
        result = temp_storage.update_book(book)
        assert result is True
        
        updated = temp_storage.get_book_by_id(book.book_id)
        assert updated.title == "Новое название"
        assert updated.status == "прочитано"
    
    def test_update_book_not_found(self, temp_storage):
        book = Book("Тест", "Тестов", 2020, book_id=999)
        result = temp_storage.update_book(book)
        assert result is False
    
    def test_delete_book(self, temp_storage):
        book = Book("Тест", "Тестов", 2020)
        temp_storage.add_book(book)
        
        result = temp_storage.delete_book(book.book_id)
        assert result is True
        
        books = temp_storage.get_all_books()
        assert len(books) == 0
    
    def test_delete_book_not_found(self, temp_storage):
        result = temp_storage.delete_book(999)
        assert result is False
    
    def test_get_all_books_empty(self, temp_storage):
        books = temp_storage.get_all_books()
        assert len(books) == 0
    
    def test_get_all_books_multiple(self, temp_storage):
        book1 = Book("Книга1", "Автор1", 2020)
        book2 = Book("Книга2", "Автор2", 2021)
        
        temp_storage.add_book(book1)
        temp_storage.add_book(book2)
        
        books = temp_storage.get_all_books()
        assert len(books) == 2
        assert any(b.title == "Книга1" for b in books)
        assert any(b.title == "Книга2" for b in books)
        assert books[0].book_id == 1
        assert books[1].book_id == 2
    
    def test_clear_all(self, temp_storage):
        book = Book("Тест", "Тестов", 2020)
        temp_storage.add_book(book)
        
        temp_storage.clear_all()
        books = temp_storage.get_all_books()
        assert len(books) == 0
        assert Book._last_id == 0