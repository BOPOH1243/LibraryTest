from library import Library, InvalidInputError


def add_book_action(library: Library) -> None:
    """
    Действие: добавить книгу в библиотеку.

    Args:
        library (Library): Объект библиотеки.
    """
    try:
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        year = int(input("Введите год издания книги: "))
        
        library.add_book(title, author, year)
        print("Книга успешно добавлена!")
    except ValueError:
        print("Ошибка: Год издания должен быть числом.")
    except InvalidInputError as e:
        print(f"Ошибка: {e}")


def delete_book_action(library: Library):
    """Удаление книги из библиотеки."""
    book_id = int(input("Введите ID книги для удаления: "))
    if library.delete_book(book_id):
        print("Книга успешно удалена!")
    else:
        print("Книга с таким ID не найдена.")


def find_books_action(library: Library):
    """Поиск книги в библиотеке."""
    print("Поиск книги (оставьте поле пустым, если не нужно):")
    title = input("Название: ") or None
    author = input("Автор: ") or None
    year = input("Год: ")
    year = int(year) if year.isdigit() else None

    results = library.find_books(title, author, year)
    if results:
        print("\nНайденные книги:")
        for book in results:
            print(f"{book.id}: {book.title} ({book.author}, {book.year}) - {book.status}")
    else:
        print("Книги не найдены.")


def show_all_books_action(library: Library):
    """Показ всех книг."""
    books = library.get_all_books()
    if books:
        print("\nСписок всех книг:")
        for book in books:
            print(f"{book.id}: {book.title} ({book.author}, {book.year}) - {book.status}")
    else:
        print("Библиотека пуста.")


def change_status_action(library: Library) -> None:
    """
    Действие: изменить статус книги.

    Args:
        library (Library): Объект библиотеки.
    """
    try:
        book_id = int(input("Введите ID книги: "))
        status = input('Введите новый статус ("в наличии" или "выдана"): ').strip()
        
        if library.change_status(book_id, status):
            print("Статус книги успешно изменен!")
        else:
            print("Ошибка: Книга с таким ID не найдена.")
    except ValueError:
        print("Ошибка: ID книги должен быть числом.")
    except InvalidInputError as e:
        print(f"Ошибка: {e}")


def exit_action(_library: Library):
    """Выход из программы."""
    print("Выход из программы.")
    exit()


def main():
    library = Library("library.json")

    # Словарь сценариев
    actions = {
        "1": ("Добавить книгу", add_book_action),
        "2": ("Удалить книгу", delete_book_action),
        "3": ("Найти книгу", find_books_action),
        "4": ("Показать все книги", show_all_books_action),
        "5": ("Изменить статус книги", change_status_action),
        "6": ("Выйти", exit_action),
    }

    while True:
        print("\nМеню управления библиотекой:")
        for key, (description, _) in actions.items():
            print(f"{key}. {description}")

        choice = input("Выберите действие: ")

        if choice in actions:
            _, action_function = actions[choice]
            action_function(library)
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
