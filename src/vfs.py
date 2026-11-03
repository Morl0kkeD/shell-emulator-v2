"""Виртуальная файловая система (XML, в памяти)."""
import base64
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field


@dataclass
class Node:
    name: str
    is_dir: bool = True
    content: str = ""
    owner: str = "user"
    children: dict = field(default_factory=dict)
    parent: "Node | None" = None


class VFS:
    def __init__(self):
        self.root = Node("/")
        self.cwd = self.root

    def load_from_xml(self, filepath: str):
        tree = ET.parse(filepath)
        root_elem = tree.getroot()
        self.root = Node("/")
        self.cwd = self.root

        def build(node, elem):
            for child in elem:
                name = child.get("name", "")
                is_dir = child.tag == "directory"
                content = child.get("content", "")
                owner = child.get("owner", "user")
                encoding = child.get("encoding", "")
                if encoding == "base64":
                    content = base64.b64decode(content).decode("utf-8", errors="replace")
                new_node = Node(name=name, is_dir=is_dir, content=content, owner=owner)
                new_node.parent = node
                node.children[name] = new_node
                if is_dir:
                    build(new_node, child)

        build(self.root, root_elem)

    def resolve_path(self, path: str) -> Node | None:
        if not path or path == "/":
            return self.root
        if path.startswith("/"):
            current = self.root
            parts = [p for p in path.split("/") if p]
        else:
            current = self.cwd
            parts = [p for p in path.split("/") if p]
        for part in parts:
            if part == "..":
                if current.parent:
                    current = current.parent
            elif part == ".":
                continue
            elif part in current.children:
                current = current.children[part]
            else:
                return None
        return current