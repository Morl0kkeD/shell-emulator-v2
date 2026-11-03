"""Парсер команд с поддержкой кавычек."""
import shlex


def parse(line: str) -> list[str]:
    try:
        return shlex.split(line)
    except ValueError as e:
        raise ValueError(f"Ошибка разбора: {e}")