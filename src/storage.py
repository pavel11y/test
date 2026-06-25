import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from src.models import Book

class Storage:
    def __init__(self, file_path: str = "data/library.json"):
        self.file_path = Path(file_path)
        self._ensure_data_directory()
        self._ensure_data_file()
        self._restore_last_id()
    
    def _ensure_data_directory(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _ensure_data_file(self) -> None:
        if not self.file_path.exists():
            self._save_data([])
    
    def _restore_last_id(self) -> None:
        books = self.get_all_books()
        if books:
            max_id = max(book.book_id for book in books)
            Book._last_id = max_id
    
    def _load_data(self) -> List[Dict[str, Any]]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    
    def _save_data(self, data: List[Dict[str, Any]]) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    
    def get_all_books(self) -> List[Book]:
        data = self._load_data()
        return [Book.from_dict(item) for item in data]
    
    def add_book(self, book: Book) -> None:
        books = self._load_data()
        books.append(book.to_dict())
        self._save_data(books)
    
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        books = self.get_all_books()
        for book in books:
            if book.book_id == book_id:
                return book
        return None
    
    def update_book(self, book: Book) -> bool:
        books = self._load_data()
        for i, item in enumerate(books):
            if item['id'] == book.book_id:
                books[i] = book.to_dict()
                self._save_data(books)
                return True
        return False
    
    def delete_book(self, book_id: int) -> bool:
        books = self._load_data()
        initial_length = len(books)
        books = [item for item in books if item['id'] != book_id]
        
        if len(books) < initial_length:
            self._save_data(books)
            return True
        return False
    
    def clear_all(self) -> None:
        self._save_data([])
        Book._last_id = 0