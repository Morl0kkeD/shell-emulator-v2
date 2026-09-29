"""Виртуальная файловая система в памяти."""
from __future__ import annotations

import base64
import xml.etree.ElementTree as ET

DEFAULT_MODE = 0o644


class VfsError(Exception):
    """Ошибка работы с VFS."""


class Node:
    """Узел VFS.

    :param kind: 'dir' или 'file'
    :param name: имя узла
    :param owner: владелец
    :param mode: права доступа
    """

    def __init__(
        self,
        kind: str,
        name: str,
        owner: str = "root",
        mode: int = DEFAULT_MODE,
    ) -> None:
        self.kind = kind
        self.name = name
        self.owner = owner
        self.mode = mode
        self.children: dict[str, Node] = {}
        self.parent: Node | None = None
        self.data: bytes = b""

    def add(self, child: Node) -> None:
        """Добавляет дочерний узел.

        :param child: дочерний узел
        :type child: Node
        """
        child.parent = self
        self.children[child.name] = child


def load_vfs(path: str) -> Node:
    """Загружает VFS из XML-файла.

    :param path: путь к XML
    :type path: str
    :return: корневой узел
    :rtype: Node
    :raises VfsError: если файл не найден или повреждён
    """
    try:
        tree = ET.parse(path)
    except FileNotFoundError as exc:
        raise VfsError(f"файл VFS не найден: {path}") from exc
    except ET.ParseError as exc:
        raise VfsError(f"неверный формат XML: {exc}") from exc

    root_elem = tree.getroot()
    root = Node("dir", "/")
    _build_children(root_elem, root)
    return root


def _build_children(elem: ET.Element, parent: Node) -> None:
    """Строит дочерние узлы рекурсивно.

    :param elem: XML-элемент
    :type elem: ET.Element
    :param parent: родительский узел
    :type parent: Node
    """
    for child in elem:
        if child.tag not in ("directory", "dir", "file"):
            continue
        kind = "dir" if child.tag in ("directory", "dir") else "file"
        name = child.get("name", "")
        owner = child.get("owner", "root")
        mode = int(child.get("mode", "644"), 8)
        node = Node(kind, name, owner, mode)
        if kind == "file":
            _load_file_content(child, node)
        parent.add(node)
        if kind == "dir":
            _build_children(child, node)


def _load_file_content(elem: ET.Element, node: Node) -> None:
    """Загружает содержимое файла с учётом base64.

    :param elem: XML-элемент файла
    :type elem: ET.Element
    :param node: узел файла
    :type node: Node
    """
    content = elem.get("content") or (elem.text or "")
    content = content.strip()
    if elem.get("encoding") == "base64":
        node.data = base64.b64decode(content)
    else:
        node.data = content.encode("utf-8")
