"""Реализация команд."""
from .vfs import VFS, Node


class CommandError(Exception):
    pass


def execute_command(vfs: VFS, cmd: str, args: list[str]) -> str:
    if cmd == "ls":
        return cmd_ls(vfs, args)
    elif cmd == "cd":
        return cmd_cd(vfs, args)
    elif cmd == "du":
        return cmd_du(vfs, args)
    elif cmd == "wc":
        return cmd_wc(vfs, args)
    elif cmd == "echo":
        return " ".join(args)
    elif cmd == "touch":
        return cmd_touch(vfs, args)
    elif cmd == "chown":
        return cmd_chown(vfs, args)
    else:
        raise CommandError(f"{cmd}: команда не найдена")


def cmd_ls(vfs, args):
    path = args[0] if args else "."
    node = vfs.resolve_path(path)
    if not node:
        raise CommandError(f"ls: {path}: нет такого файла или каталога")
    if not node.is_dir:
        return node.name
    return "  ".join(sorted(node.children.keys())) if node.children else ""


def cmd_cd(vfs, args):
    if len(args) != 1:
        raise CommandError("cd: неверное число аргументов")
    path = args[0]
    node = vfs.resolve_path(path)
    if not node:
        raise CommandError(f"cd: {path}: нет такого файла или каталога")
    if not node.is_dir:
        raise CommandError(f"cd: {path}: не каталог")
    vfs.cwd = node
    return ""


def cmd_du(vfs, args):
    path = args[0] if args else "."
    node = vfs.resolve_path(path)
    if not node:
        raise CommandError(f"du: {path}: нет такого файла или каталога")
    size = len(node.content.encode()) if not node.is_dir else sum(
        len(c.content.encode()) for c in node.children.values() if not c.is_dir
    )
    return f"{size}\t{path}"


def cmd_wc(vfs, args):
    if not args:
        raise CommandError("wc: не указан файл")
    path = args[0]
    node = vfs.resolve_path(path)
    if not node:
        raise CommandError(f"wc: {path}: нет такого файла или каталога")
    if node.is_dir:
        raise CommandError(f"wc: {path}: это каталог")
    lines = node.content.count("\n")
    words = len(node.content.split())
    chars = len(node.content)
    return f"{lines}\t{words}\t{chars}\t{path}"


def cmd_touch(vfs, args):
    if not args:
        raise CommandError("touch: использование: touch файл")
    for path in args:
        parts = [p for p in path.split("/") if p]
        current = vfs.cwd
        for part in parts[:-1]:
            if part in current.children and current.children[part].is_dir:
                current = current.children[part]
            else:
                raise CommandError(f"touch: {path}: нет такого каталога")
        name = parts[-1]
        if name in current.children:
            continue
        new_node = Node(name=name, is_dir=False)
        new_node.parent = current
        current.children[name] = new_node
    return ""


def cmd_chown(vfs, args):
    if len(args) != 2:
        raise CommandError("chown: использование: chown пользователь файл")
    user, path = args
    node = vfs.resolve_path(path)
    if not node:
        raise CommandError(f"chown: {path}: нет такого файла")
    node.owner = user
    return ""