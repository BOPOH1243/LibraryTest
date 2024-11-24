from library import Library


def main():
    library = Library("library.json")

    while True:
        print("\nМеню управления библиотекой:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие (1-6): ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания книги: "))
            library.add_book(title, author, year)
            print("Книга успешно добавлена!")

        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            if library.delete_book(book_id):
                print("Книга успешно удалена!")
            else:
                print("Книга с таким ID не найдена.")

        elif choice == "3":
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

        elif choice == "4":
            books = library.get_all_books()
            if books:
                print("\nСписок всех книг:")
                for book in books:
                    print(f"{book.id}: {book.title} ({book.author}, {book.year}) - {book.status}")
            else:
                print("Библиотека пуста.")

        elif choice == "5":
            book_id = int(input("Введите ID книги: "))
            new_status = input("Введите новый статус (в наличии/выдана): ")
            if library.change_status(book_id, new_status):
                print("Статус книги успешно обновлен!")
            else:
                print("Книга с таким ID не найдена.")

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
