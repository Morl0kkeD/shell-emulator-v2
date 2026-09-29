"""Команды эмулятора."""
from __future__ import annotations

from src.vfs import Node

NEWLINE = "\n"


class CommandError(Exception):
    """Ошибка выполнения команды."""


def resolve(cwd: Node, path: str) -> Node | None:
    """Разрешает путь относительно cwd.

    :param cwd: текущий каталог
    :type cwd: Node
    :param path: путь
    :type path: str
    :return: узел или None
    :rtype: Node | None
    """
    if path in ("", "."):
        return cwd
    node = cwd if not path.startswith("/") else _root(cwd)
    for part in path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            node = node.parent or node
            continue
        nxt = node.children.get(part)
        if nxt is None:
            return None
        node = nxt
    return node


def _root(node: Node) -> Node:
    """Возвращает корень VFS.

    :param node: узел
    :type node: Node
    :return: корень
    :rtype: Node
    """
    while node.parent is not None:
        node = node.parent
    return node


def cmd_ls(args: list[str], cwd: Node) -> tuple[str, Node]:
    """Реализация ls.

    :param args: аргументы
    :type args: list[str]
    :param cwd: текущий каталог
    :type cwd: Node
    :return: (вывод, cwd)
    :rtype: tuple[str, Node]
    """
    targets = [a for a in args if not a.startswith("-")] or ["."]
    lines: list[str] = []
    for target in targets:
        node = resolve(cwd, target)
        if node is None:
            raise CommandError(f"ls: {target}: нет такого файла")
        if node.kind == "file":
            lines.append(node.name)
        else:
            lines.extend(sorted(node.children))
    return NEWLINE.join(lines), cwd


def cmd_cd(args: list[str], cwd: Node) -> tuple[str, Node]:
    """Реализация cd.

    :param args: аргументы
    :type args: list[str]
    :param cwd: текущий каталог
    :type cwd: Node
    :return: (вывод, новый cwd)
    :rtype: tuple[str, Node]
    """
    if not args:
        return "", _root(cwd)
    target = resolve(cwd, args[0])
    if target is None or target.kind != "dir":
        raise CommandError(f"cd: {args[0]}: не каталог")
    return "", target


def cmd_du(args: list[str], cwd: Node) -> tuple[str, Node]:
    """Реализация du.

    :param args: аргументы
    :type args: list[str]
    :param cwd: текущий каталог
    :type cwd: Node
    :return: (вывод, cwd)
    :rtype: tuple[str, Node]
    """
    target = resolve(cwd, args[0]) if args else cwd
    if target is None:
        raise CommandError("du: нет такого файла")
    return f"{_du_size(target)}\t{target.name}", cwd


def _du_size(node: Node) -> int:
    """Рекурсивный размер.

    :param node: узел
    :type node: Node
    :return: размер в байтах
    :rtype: int
    """
    if node.kind == "file":
        return len(node.data)
    return sum(_du_size(c) for c in node.children.values())


def cmd_wc(args: list[str], cwd: Node) -> tuple[str, Node]:
    """Реализация wc.

    :param args: аргументы
    :type args: list[str]
    :param cwd: текущий каталог
    :type cwd: Node
    :return: (вывод, cwd)
    :rtype: tuple[str, Node]
    """
    lines: list[str] = []
    for path in args:
        node = resolve(cwd, path)
        if node is None or node.kind != "file":
            raise CommandError(f"wc: {path}: нет такого файла")
        text = node.data.decode("utf-8", errors="replace")
        lines.append(
            f"{text.count(NEWLINE)}\t"
            f"{len(text.split())}\t"
            f"{len(text)}\t{path}"
        )
    return NEWLINE.join(lines), cwd


def cmd_echo(args: list[str], cwd: Node) -> tuple[str, Node]:
    """Реализация echo.

    :param args: аргументы
    :type args: list[str]
    :param cwd: текущий каталог
    :type cwd: Node
    :return: (вывод, cwd)
    :rtype: tuple[str, Node]
    """
    return " ".join(args), cwd