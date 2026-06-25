import pytest
import tempfile
from pathlib import Path
from src.library import Library
from src.storage import Storage
from src.models import Book

class TestLibrary:
    @pytest.fixture(autouse=True)
    def reset_ids(self):
        Book._last_id = 0
        yield
        Book._last_id = 0
    
    @pytest.fixture
    def library(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test_library.json"
            storage = Storage(str(file_path))
            library = Library(storage)
            yield library
    
    def test_add_book_valid(self, library):
        book = library.add_book("Тест", "Тестов", 2020)
        
        assert book.title == "Тест"
        assert book.author == "Тестов"
        assert book.year == 2020
        assert book.status == "не прочитано"
        
        books = library.get_all_books()
        assert len(books) == 1
    
    def test_add_book_empty_title(self, library):
        with pytest.raises(ValueError) as excinfo:
            library.add_book("", "Тестов", 2020)
        assert "Название книги не может быть пустым" in str(excinfo.value)
    
    def test_add_book_empty_author(self, library):
        with pytest.raises(ValueError) as excinfo:
            library.add_book("Тест", "", 2020)
        assert "Автор книги не может быть пустым" in str(excinfo.value)
    
    def test_add_book_invalid_year(self, library):
        with pytest.raises(ValueError) as excinfo:
            library.add_book("Тест", "Тестов", -1)
        assert "Год издания должен быть положительным числом" in str(excinfo.value)
        
        with pytest.raises(ValueError) as excinfo:
            library.add_book("Тест", "Тестов", 2027)
        assert "Год издания должен быть положительным числом не более 2026" in str(excinfo.value)
    
    def test_add_book_invalid_status(self, library):
        with pytest.raises(ValueError) as excinfo:
            library.add_book("Тест", "Тестов", 2020, "в процессе")
        assert "Статус должен быть" in str(excinfo.value)
    
    def test_get_all_books_empty(self, library):
        books = library.get_all_books()
        assert len(books) == 0
    
    def test_get_all_books_with_books(self, library):
        library.add_book("Книга1", "Автор1", 2020)
        library.add_book("Книга2", "Автор2", 2021)
        
        books = library.get_all_books()
        assert len(books) == 2
    
    def test_search_books_by_title(self, library):
        library.add_book("Война и мир", "Лев Толстой", 1869)
        library.add_book("Анна Каренина", "Лев Толстой", 1877)
        library.add_book("Преступление и наказание", "Федор Достоевский", 1866)
        
        results = library.search_books("Война")
        assert len(results) == 1
        assert results[0].title == "Война и мир"
    
    def test_search_books_by_author(self, library):
        library.add_book("Война и мир", "Лев Толстой", 1869)
        library.add_book("Анна Каренина", "Лев Толстой", 1877)
        library.add_book("Преступление и наказание", "Федор Достоевский", 1866)
        
        results = library.search_books("Толстой")
        assert len(results) == 2
        assert all(b.author == "Лев Толстой" for b in results)
    
    def test_search_books_by_year(self, library):
        library.add_book("Война и мир", "Лев Толстой", 1869)
        library.add_book("Анна Каренина", "Лев Толстой", 1877)
        library.add_book("Преступление и наказание", "Федор Достоевский", 1866)
        
        results = library.search_books("1869")
        assert len(results) == 1
        assert results[0].year == 1869
    
    def test_search_books_empty_query(self, library):
        library.add_book("Книга1", "Автор1", 2020)
        library.add_book("Книга2", "Автор2", 2021)
        
        results = library.search_books("")
        assert len(results) == 2
        
        results = library.search_books("   ")
        assert len(results) == 2
    
    def test_search_books_no_results(self, library):
        library.add_book("Книга1", "Автор1", 2020)
        
        results = library.search_books("несуществующий запрос")
        assert len(results) == 0
    
    def test_filter_by_status_read(self, library):
        library.add_book("Книга1", "Автор1", 2020, "прочитано")
        library.add_book("Книга2", "Автор2", 2021, "не прочитано")
        library.add_book("Книга3", "Автор3", 2022, "прочитано")
        
        results = library.filter_by_status("прочитано")
        assert len(results) == 2
        assert all(b.status == "прочитано" for b in results)
    
    def test_filter_by_status_unread(self, library):
        library.add_book("Книга1", "Автор1", 2020, "прочитано")
        library.add_book("Книга2", "Автор2", 2021, "не прочитано")
        library.add_book("Книга3", "Автор3", 2022, "не прочитано")
        
        results = library.filter_by_status("не прочитано")
        assert len(results) == 2
        assert all(b.status == "не прочитано" for b in results)
    
    def test_filter_by_status_invalid(self, library):
        with pytest.raises(ValueError) as excinfo:
            library.filter_by_status("в процессе")
        assert "Статус должен быть" in str(excinfo.value)
    
    def test_update_book_status_valid(self, library):
        book = library.add_book("Тест", "Тестов", 2020)
        
        result = library.update_book_status(book.book_id, "прочитано")
        assert result is True
        
        updated = library.storage.get_book_by_id(book.book_id)
        assert updated.status == "прочитано"
    
    def test_update_book_status_not_found(self, library):
        with pytest.raises(ValueError) as excinfo:
            library.update_book_status(999999, "прочитано")
        assert "Книга с ID 999999 не найдена" in str(excinfo.value)
    
    def test_update_book_status_invalid(self, library):
        book = library.add_book("Тест", "Тестов", 2020)
        
        with pytest.raises(ValueError) as excinfo:
            library.update_book_status(book.book_id, "в процессе")
        assert "Статус должен быть" in str(excinfo.value)
    
    def test_delete_book_valid(self, library):
        book = library.add_book("Тест", "Тестов", 2020)
        
        result = library.delete_book(book.book_id)
        assert result is True
        
        books = library.get_all_books()
        assert len(books) == 0
    
    def test_delete_book_not_found(self, library):
        with pytest.raises(ValueError) as excinfo:
            library.delete_book(999999)
        assert "Книга с ID 999999 не найдена" in str(excinfo.value)
    
    def test_get_statistics_empty(self, library):
        stats = library.get_statistics()
        assert stats['total'] == 0
        assert stats['read'] == 0
        assert stats['unread'] == 0
    
    def test_get_statistics_with_books(self, library):
        library.add_book("Книга1", "Автор1", 2020, "прочитано")
        library.add_book("Книга2", "Автор2", 2021, "не прочитано")
        library.add_book("Книга3", "Автор3", 2022, "прочитано")
        
        stats = library.get_statistics()
        assert stats['total'] == 3
        assert stats['read'] == 2
        assert stats['unread'] == 1