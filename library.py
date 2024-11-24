import json
from typing import List, Optional, Dict


class Book:
    """
    Класс, представляющий книгу.

    Атрибуты:
        id (int): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (str): Статус книги ("в наличии" или "выдана").
    """

    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        """
        Инициализация книги.

        Args:
            book_id (int): Уникальный идентификатор книги.
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            status (str, optional): Статус книги. По умолчанию "в наличии".
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict[str, str | int]:
        """
        Преобразует объект книги в словарь.

        Returns:
            Dict[str, str | int]: Словарь с данными о книге.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict[str, str | int]) -> 'Book':
        """
        Создает объект книги из словаря.

        Args:
            data (Dict[str, str | int]): Словарь с данными о книге.

        Returns:
            Book: Объект книги.
        """
        return Book(data["id"], data["title"], data["author"], data["year"], data["status"])


class Library:
    """
    Класс для управления библиотекой книг.

    Атрибуты:
        filename (str): Имя файла для хранения данных о книгах.
        books (List[Book]): Список книг в библиотеке.
    """

    def __init__(self, filename: str):
        """
        Инициализация библиотеки.

        Args:
            filename (str): Имя файла для хранения данных.
        """
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """
        Загружает книги из файла. Если файл не существует или поврежден, список книг очищается.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self) -> None:
        """
        Сохраняет текущие книги в файл.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет новую книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """
        book_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def delete_book(self, book_id: int) -> bool:
        """
        Удаляет книгу по ID.

        Args:
            book_id (int): Уникальный идентификатор книги.

        Returns:
            bool: True, если книга успешно удалена, иначе False.
        """
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def find_books(self, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> List[Book]:
        """
        Ищет книги по названию, автору или году.

        Args:
            title (Optional[str], optional): Название книги. По умолчанию None.
            author (Optional[str], optional): Автор книги. По умолчанию None.
            year (Optional[int], optional): Год издания книги. По умолчанию None.

        Returns:
            List[Book]: Список найденных книг.
        """
        return [
            book for book in self.books
            if (title is None or title.lower() in book.title.lower()) and
               (author is None or author.lower() in book.author.lower()) and
               (year is None or book.year == year)
        ]

    def change_status(self, book_id: int, status: str) -> bool:
        """
        Изменяет статус книги.

        Args:
            book_id (int): Уникальный идентификатор книги.
            status (str): Новый статус книги ("в наличии" или "выдана").

        Returns:
            bool: True, если статус успешно изменен, иначе False.
        """
        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.save_books()
                return True
        return False

    def get_all_books(self) -> List[Book]:
        """
        Возвращает список всех книг.

        Returns:
            List[Book]: Список всех книг.
        """
        return self.books
