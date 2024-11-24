import unittest
from library import Library, Book


class TestLibrary(unittest.TestCase):
    def setUp(self):
        """Инициализация временной библиотеки перед каждым тестом."""
        self.library = Library("test_library.json")
        self.library.books = []  # Очищаем библиотеку

    def tearDown(self):
        """Очищение библиотеки после каждого теста."""
        self.library.books = []
        self.library.save_books()

    def test_add_book(self):
        """Проверка добавления книги."""
        self.library.add_book("Название", "Автор", 2023)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Название")
        self.assertEqual(self.library.books[0].author, "Автор")
        self.assertEqual(self.library.books[0].year, 2023)
        self.assertEqual(self.library.books[0].status, "в наличии")

    def test_delete_book(self):
        """Проверка удаления книги."""
        self.library.add_book("Название", "Автор", 2023)
        book_id = self.library.books[0].id
        result = self.library.delete_book(book_id)
        self.assertTrue(result)
        self.assertEqual(len(self.library.books), 0)

        # Попытка удалить несуществующую книгу
        result = self.library.delete_book(book_id)
        self.assertFalse(result)

    def test_find_books(self):
        """Проверка поиска книг."""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        self.library.add_book("Книга 2", "Автор 2", 2021)

        # Поиск по названию
        results = self.library.find_books(title="Книга 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Книга 1")

        # Поиск по автору
        results = self.library.find_books(author="Автор 2")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Автор 2")

        # Поиск по году
        results = self.library.find_books(year=2020)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].year, 2020)

        # Поиск без результатов
        results = self.library.find_books(title="Несуществующая книга")
        self.assertEqual(len(results), 0)

    def test_change_status(self):
        """Проверка изменения статуса книги."""
        self.library.add_book("Книга", "Автор", 2023)
        book_id = self.library.books[0].id

        # Изменение статуса
        result = self.library.change_status(book_id, "выдана")
        self.assertTrue(result)
        self.assertEqual(self.library.books[0].status, "выдана")

        # Попытка изменить статус несуществующей книги
        result = self.library.change_status(999, "выдана")
        self.assertFalse(result)

    def test_get_all_books(self):
        """Проверка получения всех книг."""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        self.library.add_book("Книга 2", "Автор 2", 2021)

        books = self.library.get_all_books()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, "Книга 1")
        self.assertEqual(books[1].title, "Книга 2")


if __name__ == "__main__":
    unittest.main()
