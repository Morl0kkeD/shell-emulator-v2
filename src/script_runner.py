"""Выполнение стартовых скриптов."""
from .commands import CommandError, execute_command
from .parser import parse


def run_script(vfs, script_path: str, out=print):
    print(f"--- Запуск скрипта: {script_path} ---")
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                out(f"> {line}")
                try:
                    tokens = parse(line)
                    if not tokens:
                        continue
                    cmd, args = tokens[0], tokens[1:]
                    if cmd == "exit":
                        return
                    result = execute_command(vfs, cmd, args)
                    if result:
                        out(result)
                except CommandError as e:
                    out(f"Ошибка: {e}")
                except Exception as e:
                    out(f"Ошибка выполнения: {e}")
        print("--- Скрипт завершён ---")
    except FileNotFoundError:
        print(f"Ошибка: файл скрипта '{script_path}' не найден")