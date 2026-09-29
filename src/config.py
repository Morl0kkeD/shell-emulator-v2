"""Разбор параметров командной строки."""
import argparse
from dataclasses import dataclass


@dataclass
class Config:
    """Параметры запуска эмулятора.

    :param vfs: путь к XML-файлу VFS
    :param script: путь к стартовому скрипту
    """

    vfs: str | None = None
    script: str | None = None


def parse_args(argv: list[str] | None = None) -> Config:
    """Разбирает аргументы командной строки.

    :param argv: список аргументов (по умолчанию sys.argv[1:])
    :type argv: list[str] | None
    :return: конфигурация
    :rtype: Config
    """
    parser = argparse.ArgumentParser(prog="shell-emulator")
    parser.add_argument("--vfs", help="путь к XML-файлу VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    ns = parser.parse_args(argv)
    return Config(vfs=ns.vfs, script=ns.script)


def debug_dump(cfg: Config) -> str:
    """Формирует отладочный вывод параметров.

    :param cfg: конфигурация
    :type cfg: Config
    :return: строка с параметрами
    :rtype: str
    """
    return f"[DEBUG] VFS: {cfg.vfs}\n[DEBUG] Script: {cfg.script}"
