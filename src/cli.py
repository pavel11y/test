import sys
from typing import Optional
from src.library import Library
from src.storage import Storage


DEBUG = False


def clear_screen():
    # Убрано очищение экрана
    pass


def print_colored(text='', color_code=0, end='\n', flush=True):
    # Убраны ANSI-коды, просто печатаем текст
    print(text, end=end, flush=flush)


def text_animation(text, delay=0.05, color_code=0):
    # Убрана анимация, просто печатаем текст
    print(text)


def print_title(title):
    # Убрано оформление с рамками
    print(f'\n=== БИБЛИОТЕКА КНИГ - {title.upper()} ===\n')


class ConsoleUI:
    
    def __init__(self, library: Library):
        self.library = library
        self.running = True
    
    def _print_header(self, title: str):
        print(f'\n{title}')
        print('-' * 40)
    
    def _print_success(self, message: str):
        print(f'[+] {message}')
    
    def _print_error(self, message: str):
        print(f'[!] {message}')
    
    def _print_info(self, message: str):
        print(f'[*] {message}')
    
    def _print_cancel(self, message: str):
        print(f'[-] {message}')
    
    def _print_item(self, number: int, text: str):
        print(f'{number}. {text}')
    
    def display_menu(self) -> None:
        print_title('ГЛАВНОЕ МЕНЮ')
        
        print('1. Добавить книгу')
        print('2. Показать все книги')
        print('3. Поиск книг')
        print('4. Фильтр по статусу')
        print('5. Обновить статус книги')
        print('6. Удалить книгу')
        print('7. Показать статистику')
        print('0. Выйти')
        print()
    
    def get_input(self, prompt: str, required: bool = True) -> Optional[str]:
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value if value else None
            self._print_error('Это поле обязательно для заполнения!')
    
    def get_int_input(self, prompt: str, min_val: int = None, 
                      max_val: int = None) -> Optional[int]:
        while True:
            try:
                value = input(prompt).strip()
                if not value:
                    return None
                num = int(value)
                if min_val is not None and num < min_val:
                    self._print_error(f'Значение должно быть не меньше {min_val}')
                    continue
                if max_val is not None and num > max_val:
                    self._print_error(f'Значение должно быть не больше {max_val}')
                    continue
                return num
            except ValueError:
                self._print_error('Пожалуйста, введите целое число!')
    
    def add_book_flow(self) -> None:
        print_title('ДОБАВЛЕНИЕ КНИГИ')
        
        title = self.get_input('Название книги: ')
        if not title:
            return
        
        author = self.get_input('Автор: ')
        if not author:
            return
        
        year = self.get_int_input('Год издания: ', min_val=0, max_val=2026)
        if year is None:
            return
        
        print()
        print('Выберите статус:')
        self._print_item(1, 'Не прочитано')
        self._print_item(2, 'Прочитано')
        print()
        
        status_choice = self.get_int_input('Ваш выбор (1 или 2): ', min_val=1, max_val=2)
        if status_choice is None:
            return
        
        status = 'не прочитано' if status_choice == 1 else 'прочитано'
        
        try:
            book = self.library.add_book(title, author, year, status)
            self._print_success('Книга успешно добавлена!')
            print(f'  {book}')
        except ValueError as e:
            self._print_error(str(e))
    
    def display_books(self, books: list, title: str = 'Список книг') -> None:
        print_title(title)
        
        if not books:
            self._print_info('Нет книг для отображения')
            return
        
        for i, book in enumerate(books, 1):
            print(f'{i}. {book}')
        
        print()
        print('-' * 40)
        print(f'Всего: {len(books)} книг')
        print()
        input('Нажмите Enter для продолжения...')
    
    def show_all_books_flow(self) -> None:
        books = self.library.get_all_books()
        self.display_books(books, 'ВСЕ КНИГИ')
    
    def search_books_flow(self) -> None:
        print_title('ПОИСК КНИГ')
        print('Поиск по названию, автору или году')
        print()
        
        query = self.get_input('Поисковый запрос: ', required=False)
        if query is None:
            return
        
        books = self.library.search_books(query)
        self.display_books(books, f"РЕЗУЛЬТАТЫ ПОИСКА: '{query}'")
    
    def filter_books_flow(self) -> None:
        print_title('ФИЛЬТРАЦИЯ ПО СТАТУСУ')
        self._print_item(1, 'Не прочитано')
        self._print_item(2, 'Прочитано')
        print()
        
        choice = self.get_int_input('Ваш выбор (1 или 2): ', min_val=1, max_val=2)
        if choice is None:
            return
        
        status = 'не прочитано' if choice == 1 else 'прочитано'
        
        try:
            books = self.library.filter_by_status(status)
            self.display_books(books, f"КНИГИ СО СТАТУСОМ: '{status}'")
        except ValueError as e:
            self._print_error(str(e))
    
    def update_status_flow(self) -> None:
        print_title('ОБНОВЛЕНИЕ СТАТУСА')
        
        book_id = self.get_int_input('ID книги: ', min_val=1)
        if book_id is None:
            return
        
        book = self.library.storage.get_book_by_id(book_id)
        if not book:
            self._print_error(f'Книга с ID {book_id} не найдена')
            return
        
        self._print_info('Текущая книга:')
        print(f'  {book}')
        print()
        
        print('Выберите новый статус:')
        self._print_item(1, 'Не прочитано')
        self._print_item(2, 'Прочитано')
        print()
        
        choice = self.get_int_input('Ваш выбор (1 или 2): ', min_val=1, max_val=2)
        if choice is None:
            return
        
        new_status = 'не прочитано' if choice == 1 else 'прочитано'
        
        try:
            if self.library.update_book_status(book_id, new_status):
                self._print_success('Статус книги обновлен!')
                updated = self.library.storage.get_book_by_id(book_id)
                print(f'  {updated}')
            else:
                self._print_error('Не удалось обновить статус')
        except ValueError as e:
            self._print_error(str(e))
    
    def delete_book_flow(self) -> None:
        print_title('УДАЛЕНИЕ КНИГИ')
        
        book_id = self.get_int_input('ID книги для удаления: ', min_val=1)
        if book_id is None:
            return
        
        book = self.library.storage.get_book_by_id(book_id)
        if book:
            self._print_info('Книга для удаления:')
            print(f'  {book}')
            print()
            confirm = input('Вы уверены? (y/n): ').strip().lower()
            if confirm != 'y':
                self._print_cancel('Удаление отменено')
                return
        else:
            self._print_error(f'Книга с ID {book_id} не найдена')
            return
        
        try:
            if self.library.delete_book(book_id):
                self._print_success('Книга успешно удалена!')
            else:
                self._print_error('Не удалось удалить книгу')
        except ValueError as e:
            self._print_error(str(e))
    
    def show_statistics_flow(self) -> None:
        stats = self.library.get_statistics()
        print_title('СТАТИСТИКА')
        
        print(f'  Всего книг:     {stats["total"]}')
        print(f'  Прочитано:      {stats["read"]}')
        print(f'  Не прочитано:   {stats["unread"]}')
        
        if stats['total'] > 0:
            progress = (stats['read'] / stats['total']) * 100
            print(f'  Прогресс:       {progress:.1f}%')
        
        print()
        input('Нажмите Enter для продолжения...')
    
    def run(self) -> None:
        print_title('ДОБРО ПОЖАЛОВАТЬ!')
        print('Система управления библиотекой загружена...')
        
        while self.running:
            self.display_menu()
            choice = self.get_int_input('Выберите опцию: ')
            
            if choice is None:
                continue
            
            if choice == 0:
                print_title('ДО СВИДАНИЯ!')
                print('Спасибо за использование библиотеки!')
                self.running = False
            elif choice == 1:
                self.add_book_flow()
            elif choice == 2:
                self.show_all_books_flow()
            elif choice == 3:
                self.search_books_flow()
            elif choice == 4:
                self.filter_books_flow()
            elif choice == 5:
                self.update_status_flow()
            elif choice == 6:
                self.delete_book_flow()
            elif choice == 7:
                self.show_statistics_flow()
            else:
                self._print_error('Неверный выбор! Пожалуйста, выберите опцию от 0 до 7')


def main():
    try:
        storage = Storage()
        library = Library(storage)
        ui = ConsoleUI(library)
        ui.run()
    except KeyboardInterrupt:
        print('\n\nПрограмма прервана пользователем')
        sys.exit(0)
    except Exception as e:
        print(f'\n[КРИТИЧЕСКАЯ ОШИБКА] {e}')
        if DEBUG:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()