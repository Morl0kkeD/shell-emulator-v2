"""Графический интерфейс эмулятора."""
import getpass
import socket
import tkinter as tk
from tkinter import scrolledtext

from src.parser import ParseError, parse


class ShellGUI:
    """Окно эмулятора с полем ввода и областью вывода."""

    def __init__(self) -> None:
        """Создаёт окно и виджеты."""
        self.root = tk.Tk()
        user = getpass.getuser()
        host = socket.gethostname()
        title = f"Эмулятор - [{user}@{host}]"
        self.root.title(title)
        self.root.geometry("800x500")

        self.out = scrolledtext.ScrolledText(
            self.root, state="disabled", wrap="word"
        )
        self.out.pack(fill="both", expand=True)

        self.inp = tk.Entry(self.root)
        self.inp.pack(fill="x")
        self.inp.bind("<Return>", self.on_enter)
        self.inp.focus_set()

    def write(self, text: str) -> None:
        """Добавляет строку в область вывода.

        :param text: текст для вывода
        :type text: str
        """
        self.out.configure(state="normal")
        self.out.insert("end", text + "\n")
        self.out.configure(state="disabled")
        self.out.see("end")

    def on_enter(self, _event) -> None:
        """Обрабатывает Enter в поле ввода.

        :param _event: событие Tkinter
        """
        line = self.inp.get()
        self.inp.delete(0, "end")
        if not line.strip():
            return
        self.write(f"> {line}")
        self.dispatch(line)

    def dispatch(self, line: str) -> None:
        """Разбирает и выполняет строку.

        :param line: введённая строка
        :type line: str
        """
        try:
            tokens = parse(line)
        except ParseError as exc:
            self.write(f"Ошибка: {exc}")
            return
        if not tokens:
            return
        self.run_tokens(tokens)

    def run_tokens(self, tokens: list[str]) -> None:
        """Выполняет команду (заглушки этапа 1).

        :param tokens: список токенов
        :type tokens: list[str]
        """
        name, *args = tokens
        if name == "exit":
            self.root.destroy()
            return
        if name in ("ls", "cd"):
            self.write(f"{name}: аргументы {args}")
            return
        self.write(f"{name}: команда не найдена")

    def set_vfs(self, path: str) -> None:
        """Показывает, что VFS будет загружен (заглушка этапа 2).

        :param path: путь к XML
        :type path: str
        """
        self.write(f"[VFS] будет загружен: {path}")

    def run_script_file(self, path: str) -> None:
        """Выполняет стартовый скрипт.

        :param path: путь к скрипту
        :type path: str
        """
        from src.script_runner import run_script

        run_script(path, self.dispatch, self.write)

    def run(self) -> None:
        """Запускает главный цикл."""
        self.root.mainloop()
