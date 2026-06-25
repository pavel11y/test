import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional
from src.library import Library
from src.storage import Storage

class LibraryGUI:
    def __init__(self, library: Library):
        self.library = library
        self.window = tk.Tk()
        self.window.title("Библиотека книг")
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        
        self.setup_styles()
        self.create_widgets()
        self.refresh_books_list()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TButton', font=('Arial', 10))
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Управление библиотекой", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        control_frame = ttk.LabelFrame(main_frame, text="Действия", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X)
        
        self.add_btn = ttk.Button(btn_frame, text="Добавить книгу", command=self.add_book_window, width=18)
        self.add_btn.pack(side=tk.LEFT, padx=2)
        
        self.search_btn = ttk.Button(btn_frame, text="Поиск", command=self.search_window, width=15)
        self.search_btn.pack(side=tk.LEFT, padx=2)
        
        self.filter_btn = ttk.Button(btn_frame, text="Фильтр", command=self.filter_window, width=15)
        self.filter_btn.pack(side=tk.LEFT, padx=2)
        
        self.stats_btn = ttk.Button(btn_frame, text="Статистика", command=self.show_statistics, width=15)
        self.stats_btn.pack(side=tk.LEFT, padx=2)
        
        self.refresh_btn = ttk.Button(btn_frame, text="Обновить", command=self.refresh_books_list, width=15)
        self.refresh_btn.pack(side=tk.LEFT, padx=2)
        
        list_frame = ttk.LabelFrame(main_frame, text="Список книг", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        columns = ('ID', 'Название', 'Автор', 'Год', 'Статус')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Название', text='Название')
        self.tree.heading('Автор', text='Автор')
        self.tree.heading('Год', text='Год')
        self.tree.heading('Статус', text='Статус')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Название', width=250)
        self.tree.column('Автор', width=200)
        self.tree.column('Год', width=80, anchor='center')
        self.tree.column('Статус', width=120, anchor='center')
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.status_btn = ttk.Button(action_frame, text="Изменить статус", command=self.update_status_window, width=20)
        self.status_btn.pack(side=tk.LEFT, padx=2)
        
        self.delete_btn = ttk.Button(action_frame, text="Удалить книгу", command=self.delete_book, width=20)
        self.delete_btn.pack(side=tk.LEFT, padx=2)
        
        self.view_btn = ttk.Button(action_frame, text="Просмотр", command=self.view_book, width=20)
        self.view_btn.pack(side=tk.LEFT, padx=2)
        
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_label = ttk.Label(status_frame, text="Готово", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X)
    
    def refresh_books_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        books = self.library.get_all_books()
        for book in books:
            status_display = "Прочитано" if book.status == "прочитано" else "Не прочитано"
            self.tree.insert('', tk.END, values=(
                book.book_id,
                book.title,
                book.author,
                book.year,
                status_display
            ))
        
        self.status_label.config(text=f"Всего книг: {len(books)}")
    
    def add_book_window(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Добавление книги")
        dialog.geometry("400x400")
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Добавление новой книги", style='Header.TLabel').pack(pady=(0, 15))
        
        ttk.Label(main_frame, text="Название:").pack(anchor=tk.W, pady=(0, 2))
        title_entry = ttk.Entry(main_frame, width=40)
        title_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(main_frame, text="Автор:").pack(anchor=tk.W, pady=(0, 2))
        author_entry = ttk.Entry(main_frame, width=40)
        author_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(main_frame, text="Год издания:").pack(anchor=tk.W, pady=(0, 2))
        year_entry = ttk.Entry(main_frame, width=40)
        year_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(main_frame, text="Статус:").pack(anchor=tk.W, pady=(0, 2))
        status_var = tk.StringVar(value="не прочитано")
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Radiobutton(status_frame, text="Не прочитано", variable=status_var, 
                       value="не прочитано").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(status_frame, text="Прочитано", variable=status_var, 
                       value="прочитано").pack(side=tk.LEFT, padx=5)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        def submit():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            year_str = year_entry.get().strip()
            
            if not title:
                messagebox.showerror("Ошибка", "Название книги не может быть пустым")
                return
            if not author:
                messagebox.showerror("Ошибка", "Автор книги не может быть пустым")
                return
            if not year_str:
                messagebox.showerror("Ошибка", "Введите год издания")
                return
            
            try:
                year = int(year_str)
                if year < 0 or year > 2026:
                    messagebox.showerror("Ошибка", "Год должен быть от 0 до 2026")
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректный год")
                return
            
            try:
                self.library.add_book(title, author, year, status_var.get())
                self.refresh_books_list()
                dialog.destroy()
                messagebox.showinfo("Успех", "Книга успешно добавлена!")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        ttk.Button(btn_frame, text="Добавить", command=submit, width=15).pack(side=tk.RIGHT, padx=2)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.RIGHT, padx=2)
        
        title_entry.focus()
    
    def search_window(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Поиск книг")
        dialog.geometry("450x150")
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Поиск по названию, автору или году", style='Header.TLabel').pack(pady=(0, 10))
        
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        search_entry = ttk.Entry(search_frame, width=35)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        def do_search():
            query = search_entry.get().strip()
            if not query:
                self.refresh_books_list()
                dialog.destroy()
                return
            
            books = self.library.search_books(query)
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for book in books:
                status_display = "Прочитано" if book.status == "прочитано" else "Не прочитано"
                self.tree.insert('', tk.END, values=(
                    book.book_id,
                    book.title,
                    book.author,
                    book.year,
                    status_display
                ))
            
            self.status_label.config(text=f"Найдено: {len(books)} книг")
            dialog.destroy()
        
        ttk.Button(search_frame, text="Искать", command=do_search, width=12).pack(side=tk.LEFT)
        ttk.Button(main_frame, text="Отмена", command=dialog.destroy, width=15).pack()
        
        search_entry.focus()
        search_entry.bind('<Return>', lambda e: do_search())
    
    def filter_window(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Фильтрация по статусу")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Выберите статус для фильтрации", style='Header.TLabel').pack(pady=(0, 15))
        
        def apply_filter(status):
            books = self.library.filter_by_status(status)
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for book in books:
                status_display = "✓ Прочитано" if book.status == "прочитано" else "○ Не прочитано"
                self.tree.insert('', tk.END, values=(
                    book.book_id,
                    book.title,
                    book.author,
                    book.year,
                    status_display
                ))
            
            self.status_label.config(text=f"Отфильтровано: {len(books)} книг (статус: {status})")
            dialog.destroy()
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Не прочитано", 
                  command=lambda: apply_filter("не прочитано"), width=18).pack(pady=2)
        ttk.Button(btn_frame, text="Прочитано", 
                  command=lambda: apply_filter("прочитано"), width=18).pack(pady=2)
        ttk.Button(btn_frame, text="Сбросить фильтр", 
                  command=lambda: [self.refresh_books_list(), dialog.destroy()], width=18).pack(pady=2)
    
    def update_status_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для изменения статуса")
            return
        
        item = self.tree.item(selected[0])
        book_id = int(item['values'][0])
        book = self.library.storage.get_book_by_id(book_id)
        
        if not book:
            messagebox.showerror("Ошибка", "Книга не найдена")
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Изменение статуса")
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Книга: {book.title}", style='Header.TLabel').pack()
        ttk.Label(main_frame, text=f"Текущий статус: {book.status}").pack(pady=5)
        
        status_var = tk.StringVar(value=book.status)
        
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        ttk.Radiobutton(status_frame, text="Не прочитано", variable=status_var, 
                       value="не прочитано").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(status_frame, text="Прочитано", variable=status_var, 
                       value="прочитано").pack(side=tk.LEFT, padx=5)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        def update():
            try:
                self.library.update_book_status(book_id, status_var.get())
                self.refresh_books_list()
                dialog.destroy()
                messagebox.showinfo("Успех", "Статус книги обновлен!")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        ttk.Button(btn_frame, text="Обновить", command=update, width=15).pack(side=tk.RIGHT, padx=2)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.RIGHT, padx=2)
    
    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для удаления")
            return
        
        item = self.tree.item(selected[0])
        book_id = int(item['values'][0])
        book_title = item['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Удалить книгу '{book_title}'?"):
            try:
                self.library.delete_book(book_id)
                self.refresh_books_list()
                messagebox.showinfo("Успех", "Книга удалена!")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    def view_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для просмотра")
            return
        
        item = self.tree.item(selected[0])
        book_id = int(item['values'][0])
        book = self.library.storage.get_book_by_id(book_id)
        
        if not book:
            messagebox.showerror("Ошибка", "Книга не найдена")
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Информация о книге")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        info_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=('Arial', 11))
        info_text.pack(fill=tk.BOTH, expand=True)
        
        info = f"""
Информация о книги


ID: {book.book_id}
Название: {book.title}
Автор: {book.author}
Год издания: {book.year}
Статус: {book.status}
Добавлена: {book.created_at}
        """
        
        info_text.insert(tk.END, info)
        info_text.config(state=tk.DISABLED)
        
        ttk.Button(main_frame, text="Закрыть", command=dialog.destroy, width=15).pack(pady=10)
    
    def show_statistics(self):
        stats = self.library.get_statistics()
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Статистика библиотеки")
        dialog.geometry("350x250")
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Статистика библиотеки", style='Title.TLabel').pack(pady=(0, 15))
        
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(stats_frame, text=f"Всего книг:", font=('Arial', 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(stats_frame, text=f"{stats['total']}", font=('Arial', 12, 'bold')).grid(row=0, column=1, sticky=tk.E, pady=5, padx=(20, 0))
        
        ttk.Label(stats_frame, text=f"Прочитано:", font=('Arial', 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(stats_frame, text=f"{stats['read']}", font=('Arial', 12, 'bold'), foreground='green').grid(row=1, column=1, sticky=tk.E, pady=5, padx=(20, 0))
        
        ttk.Label(stats_frame, text=f"Не прочитано:", font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(stats_frame, text=f"{stats['unread']}", font=('Arial', 12, 'bold'), foreground='orange').grid(row=2, column=1, sticky=tk.E, pady=5, padx=(20, 0))
        
        if stats['total'] > 0:
            progress = (stats['read'] / stats['total']) * 100
            ttk.Label(stats_frame, text=f"Прогресс:", font=('Arial', 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
            ttk.Label(stats_frame, text=f"{progress:.1f}%", font=('Arial', 12, 'bold')).grid(row=3, column=1, sticky=tk.E, pady=5, padx=(20, 0))
        
        ttk.Button(main_frame, text="Закрыть", command=dialog.destroy, width=15).pack(pady=15)
    
    def run(self):
        self.window.mainloop()