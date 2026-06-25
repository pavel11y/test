from datetime import datetime
from typing import Dict, Any

class Book:
    _last_id = 0
    
    def __init__(self, title: str, author: str, year: int, 
                 status: str = "не прочитано", book_id: int = None):
        self.title = title.strip()
        self.author = author.strip()
        self.year = year
        self.status = status
        self.book_id = book_id or self._generate_id()
        self.created_at = datetime.now().isoformat()
    
    @classmethod
    def _generate_id(cls) -> int:
        cls._last_id += 1
        return cls._last_id
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.book_id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Book':
        book = cls(
            title=data['title'],
            author=data['author'],
            year=data['year'],
            status=data['status'],
            book_id=data['id']
        )
        book.created_at = data.get('created_at', datetime.now().isoformat())
        if data['id'] > cls._last_id:
            cls._last_id = data['id']
        return book
    
    def update_status(self, new_status: str) -> None:
        if new_status not in ['прочитано', 'не прочитано']:
            raise ValueError("Статус должен быть 'прочитано' или 'не прочитано'")
        self.status = new_status
    
    def __str__(self) -> str:
        return f"ID: {self.book_id} | {self.title} - {self.author} ({self.year}) | Статус: {self.status}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return False
        return self.book_id == other.book_id