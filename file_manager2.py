import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Файловый менеджер")
        self.current_directory = os.path.expanduser("~")  # Начинаем с домашней директории

        # Создаем Listbox для отображения файлов и папок
        self.listbox = Listbox(root, width=50, height=20)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Добавляем полосу прокрутки
        self.scrollbar = Scrollbar(root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Двойной клик для открытия файла или папки
        self.listbox.bind('<Double-Button-1>', self.open_item)

        # Кнопка для выбора новой папки
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.btn_open = tk.Button(self.button_frame, text="Выбрать папку", command=self.select_directory)
        self.btn_open.pack(side=tk.LEFT)

        self.btn_create_folder = tk.Button(self.button_frame, text="Создать папку", command=self.create_folder)
        self.btn_create_folder.pack(side=tk.LEFT)

        self.btn_delete = tk.Button(self.button_frame, text="Удалить", command=self.delete_item)
        self.btn_delete.pack(side=tk.LEFT)

        # Загружаем начальную директорию
        self.load_directory(self.current_directory)

    def load_directory(self, path):
        """Загружает содержимое указанной директории в Listbox."""
        self.current_directory = path
        self.listbox.delete(0, tk.END)  # Очищаем список

        try:
            for item in os.listdir(path):
                self.listbox.insert(tk.END, item)  # Добавляем элементы в список
        except PermissionError:
            messagebox.showerror("Ошибка", "Нет доступа к этой папке.")

    def open_item(self, event):
        """Открывает файл или папку при двойном клике."""
        selected_item = self.listbox.get(self.listbox.curselection())
        full_path = os.path.join(self.current_directory, selected_item)

        if os.path.isdir(full_path):
            self.load_directory(full_path)  # Загружаем содержимое папки
        else:
            os.startfile(full_path)  # Открываем файл

    def select_directory(self):
        """Выбор новой директории через диалоговое окно."""
        new_directory = filedialog.askdirectory(initialdir=self.current_directory)
        if new_directory:
            self.load_directory(new_directory)

    def create_folder(self):
        """Создает новую папку."""
        folder_name = filedialog.asksaveasfilename(title="Введите имя новой папки", defaultextension="", initialdir=self.current_directory)
        
        if folder_name:
            try:
                os.makedirs(folder_name)
                self.load_directory(self.current_directory)  # Обновляем список
            except FileExistsError:
                messagebox.showerror("Ошибка", "Папка с таким именем уже существует.")

    def delete_item(self):
        """Удаляет выбранный файл или папку."""
        selected_item = self.listbox.get(self.listbox.curselection())
        full_path = os.path.join(self.current_directory, selected_item)

        if messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить '{selected_item}'?"):
            try:
                if os.path.isdir(full_path):
                    os.rmdir(full_path)  # Удаляем пустую папку
                else:
                    os.remove(full_path)  # Удаляем файл
                self.load_directory(self.current_directory)  # Обновляем список
            except OSError as e:
                            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    file_manager = FileManager(root)
    root.mainloop()
