"""Тесты эмулятора."""
import pytest

from src.commands import CommandError, cmd_cd, cmd_ls, cmd_touch
from src.parser import ParseError, parse
from src.vfs import VfsError, load_vfs


def test_parse_plain() -> None:
    """Разбор простой строки."""
    assert parse("ls -la") == ["ls", "-la"]


def test_parse_double_quotes() -> None:
    """Разбор строки с двойными кавычками."""
    assert parse('ls "my dir"') == ["ls", "my dir"]


def test_parse_single_quotes() -> None:
    """Разбор строки с одинарными кавычками."""
    assert parse("cd 'my dir'") == ["cd", "my dir"]


def test_parse_unclosed() -> None:
    """Незакрытая кавычка — ошибка."""
    with pytest.raises(ParseError):
        parse('ls "abc')


def test_load_minimal() -> None:
    """Загрузка минимального XML."""
    root = load_vfs("test_data/minimal.xml")
    assert root.kind == "dir"
    assert "readme.txt" in root.children


def test_load_medium() -> None:
    """Загрузка medium.xml — содержимое на верхнем уровне."""
    root = load_vfs("test_data/medium.xml")
    assert "docs" in root.children
    assert "file1.txt" in root.children


def test_load_deep() -> None:
    """Загрузка deep.xml — 3 уровня вложенности."""
    root = load_vfs("test_data/deep.xml")
    assert "home" in root.children
    home = root.children["home"]
    assert "user" in home.children
    user = home.children["user"]
    assert "documents" in user.children


def test_load_missing() -> None:
    """Отсутствующий файл — ошибка."""
    with pytest.raises(VfsError):
        load_vfs("test_data/none.xml")


def test_ls_root() -> None:
    """ls в корне medium.xml."""
    root = load_vfs("test_data/medium.xml")
    out, _ = cmd_ls([], root)
    assert "docs" in out
    assert "file1.txt" in out


def test_cd_into_docs() -> None:
    """cd docs переходит в каталог."""
    root = load_vfs("test_data/medium.xml")
    _, new_cwd = cmd_cd(["docs"], root)
    assert new_cwd.name == "docs"


def test_cd_missing() -> None:
    """cd в несуществующий каталог — ошибка."""
    root = load_vfs("test_data/medium.xml")
    with pytest.raises(CommandError):
        cmd_cd(["nope"], root)


def test_touch_create() -> None:
    """touch создаёт файл."""
    root = load_vfs("test_data/medium.xml")
    cmd_touch(["new.txt"], root)
    assert "new.txt" in root.children


def test_touch_nested() -> None:
    """touch создаёт файл в подкаталоге."""
    root = load_vfs("test_data/medium.xml")
    cmd_touch(["docs/x.txt"], root)
    assert "x.txt" in root.children["docs"].children


def test_touch_missing_dir() -> None:
    """touch в несуществующий каталог — ошибка."""
    root = load_vfs("test_data/medium.xml")
    with pytest.raises(CommandError):
        cmd_touch(["nope/x.txt"], root)