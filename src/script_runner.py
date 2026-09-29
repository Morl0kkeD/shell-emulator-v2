"""Выполнение стартового скрипта."""
from collections.abc import Callable


def run_script(
    path: str,
    execute: Callable[[str], None],
    out: Callable[[str], None],
) -> None:
    """Выполняет стартовый скрипт построчно.

    Ошибочные строки пропускаются, выполнение продолжается.

    :param path: путь к скрипту
    :type path: str
    :param execute: функция выполнения строки
    :type execute: Callable[[str], None]
    :param out: функция вывода
    :type out: Callable[[str], None]
    """
    with open(path, encoding="utf-8") as file:
        for raw in file:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            out(f"> {line}")
            try:
                execute(line)
            except Exception as exc:  # noqa: BLE001
                out(f"Ошибка: {exc}")
                continue
