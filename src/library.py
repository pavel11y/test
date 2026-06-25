from typing import List, Optional
from src.models import Book
from src.storage import Storage

class Library:
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def add_book(self, title: str, author: str, year: int, status: str = "не прочитано") -> Book:
        if not title or not title.strip():
            raise ValueError("Название книги не может быть пустым")
        if not author or not author.strip():
            raise ValueError("Автор книги не может быть пустым")
        if not isinstance(year, int) or year < 0 or year > 2026:
            raise ValueError("Год издания должен быть положительным числом не более 2026")
        if status not in ['прочитано', 'не прочитано']:
            raise ValueError("Статус должен быть 'прочитано' или 'не прочитано'")
        
        book = Book(title, author, year, status)
        self.storage.add_book(book)
        return book
    
    def get_all_books(self) -> List[Book]:
        return self.storage.get_all_books()
    
    def search_books(self, query: str) -> List[Book]:
        if not query or not query.strip():
            return self.get_all_books()
        
        query = query.strip().lower()
        books = self.get_all_books()
        results = []
        
        for book in books:
            if (query in book.title.lower() or 
                query in book.author.lower() or 
                query == str(book.year)):
                results.append(book)
        
        return results
    
    def filter_by_status(self, status: str) -> List[Book]:
        if status not in ['прочитано', 'не прочитано']:
            raise ValueError("Статус должен быть 'прочитано' или 'не прочитано'")
        
        books = self.get_all_books()
        return [book for book in books if book.status == status]
    
    def update_book_status(self, book_id: int, new_status: str) -> bool:
        if new_status not in ['прочитано', 'не прочитано']:
            raise ValueError("Статус должен быть 'прочитано' или 'не прочитано'")
        
        book = self.storage.get_book_by_id(book_id)
        if not book:
            raise ValueError(f"Книга с ID {book_id} не найдена")
        
        book.update_status(new_status)
        return self.storage.update_book(book)
    
    def delete_book(self, book_id: int) -> bool:
        if not self.storage.get_book_by_id(book_id):
            raise ValueError(f"Книга с ID {book_id} не найдена")
        
        return self.storage.delete_book(book_id)
    
    def get_statistics(self) -> dict:
        books = self.get_all_books()
        total = len(books)
        read = len([b for b in books if b.status == "прочитано"])
        unread = total - read
        
        return {
            'total': total,
            'read': read,
            'unread': unread
        }