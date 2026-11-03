"""Графический интерфейс эмулятора."""
import getpass
import socket
import tkinter as tk
from tkinter import scrolledtext

from .commands import CommandError, execute_command
from .parser import parse


class EmulatorGUI:
    def __init__(self, vfs):
        self.vfs = vfs
        self.root = tk.Tk()
        username = getpass.getuser()
        hostname = socket.gethostname()
        self.root.title(f"Эмулятор - [{username}@{hostname}]")
        self.root.geometry("800x500")

        self.output = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 11), height=20
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=4, pady=(4, 0))

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.entry_var, font=("Consolas", 11), width=50)
        self.entry.pack(fill=tk.X, side=tk.BOTTOM, padx=4, pady=4)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus_set()

        self.print_line(f"Добро пожаловать в эмулятор!")

    def print_line(self, text):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def on_enter(self, event=None):
        line = self.entry_var.get()
        self.entry_var.set("")
        self.print_line(f"> {line}")
        try:
            tokens = parse(line)
            if not tokens:
                return
            cmd, args = tokens[0], tokens[1:]
            if cmd == "exit":
                self.root.destroy()
                return
            result = execute_command(self.vfs, cmd, args)
            if result:
                self.print_line(result)
        except CommandError as e:
            self.print_line(f"Ошибка: {e}")
        except Exception as e:
            self.print_line(f"Ошибка выполнения: {e}")

    def run(self):
        self.root.mainloop()