import pytest
from src.models import Book

class TestBook:
    @pytest.fixture(autouse=True)
    def reset_ids(self):
        Book._last_id = 0
        yield
        Book._last_id = 0
    
    def test_book_creation(self):
        book = Book("Война и мир", "Лев Толстой", 1869)
        
        assert book.title == "Война и мир"
        assert book.author == "Лев Толстой"
        assert book.year == 1869
        assert book.status == "не прочитано"
        assert book.book_id is not None
        assert book.created_at is not None
    
    def test_book_creation_with_status(self):
        book = Book("Преступление и наказание", "Федор Достоевский", 1866, "прочитано")
        
        assert book.title == "Преступление и наказание"
        assert book.author == "Федор Достоевский"
        assert book.year == 1866
        assert book.status == "прочитано"
    
    def test_book_trimming(self):
        book = Book("  Война и мир  ", "  Лев Толстой  ", 1869)
        
        assert book.title == "Война и мир"
        assert book.author == "Лев Толстой"
    
    def test_to_dict(self):
        book = Book("Тест", "Тестов", 2020)
        data = book.to_dict()
        
        assert data['id'] == book.book_id
        assert data['title'] == "Тест"
        assert data['author'] == "Тестов"
        assert data['year'] == 2020
        assert data['status'] == "не прочитано"
        assert 'created_at' in data
    
    def test_from_dict(self):
        data = {
            'id': 5,
            'title': 'Тест',
            'author': 'Тестов',
            'year': 2020,
            'status': 'прочитано',
            'created_at': '2024-01-01T12:00:00'
        }
        book = Book.from_dict(data)
        
        assert book.book_id == 5
        assert book.title == "Тест"
        assert book.author == "Тестов"
        assert book.year == 2020
        assert book.status == "прочитано"
        assert book.created_at == '2024-01-01T12:00:00'
    
    def test_update_status_valid(self):
        book = Book("Тест", "Тестов", 2020)
        book.update_status("прочитано")
        assert book.status == "прочитано"
        
        book.update_status("не прочитано")
        assert book.status == "не прочитано"
    
    def test_update_status_invalid(self):
        book = Book("Тест", "Тестов", 2020)
        
        with pytest.raises(ValueError) as excinfo:
            book.update_status("в процессе")
        assert "Статус должен быть" in str(excinfo.value)
    
    def test_str_representation(self):
        book = Book("Тест", "Тестов", 2020, "не прочитано", 5)
        str_repr = str(book)
        
        assert "ID: 5" in str_repr
        assert "Тест" in str_repr
        assert "Тестов" in str_repr
        assert "2020" in str_repr
        assert "не прочитано" in str_repr
    
    def test_equality(self):
        book1 = Book("Тест1", "Автор1", 2020, book_id=1)
        book2 = Book("Тест2", "Автор2", 2021, book_id=1)
        book3 = Book("Тест3", "Автор3", 2022, book_id=2)
        
        assert book1 == book2
        assert book1 != book3
        assert book1 != "не книга"
    
    def test_id_increments(self):
        book1 = Book("Книга1", "Автор1", 2020)
        book2 = Book("Книга2", "Автор2", 2021)
        book3 = Book("Книга3", "Автор3", 2022)
        
        assert book1.book_id == 1
        assert book2.book_id == 2
        assert book3.book_id == 3