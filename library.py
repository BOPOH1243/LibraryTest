import json
from typing import List, Optional, Dict


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Book':
        return Book(data["id"], data["title"], data["author"], data["year"], data["status"])


class Library:
    def __init__(self, filename: str):
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        book_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def delete_book(self, book_id: int) -> bool:
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def find_books(self, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> List[Book]:
        return [
            book for book in self.books
            if (title is None or title.lower() in book.title.lower()) and
               (author is None or author.lower() in book.author.lower()) and
               (year is None or book.year == year)
        ]

    def change_status(self, book_id: int, status: str) -> bool:
        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.save_books()
                return True
        return False

    def get_all_books(self) -> List[Book]:
        return self.books
