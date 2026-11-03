# Эмулятор командной оболочки ОС (Вариант №36)

## Общее описание

GUI-эмулятор UNIX-подобной командной оболочки с виртуальной
файловой системой (VFS) на основе XML. Все операции VFS
выполняются в памяти, двоичные данные кодируются в base64.

Возможности:
- REPL с графическим интерфейсом (Tkinter)
- заголовок окна `Эмулятор - [username@hostname]`
- парсер с поддержкой аргументов в кавычках
- конфигурация через `--vfs` и `--script`
- стартовые скрипты с пропуском ошибочных строк
- виртуальная файловая система из XML
- команды: `ls`, `cd`, `du`, `wc`, `echo`, `touch`, `chown`, `exit`

## Функции и настройки

Параметры командной строки:

- `--vfs PATH` — путь к XML-файлу VFS
- `--script PATH` — путь к стартовому скрипту

Формат XML VFS:

    <?xml version="1.0" encoding="UTF-8"?>
    <vfs name="example">
      <directory name="docs">
        <file name="doc1.txt" content="Hello"/>
      </directory>
      <file name="file1.txt" content="World"/>
      <file name="encoded.bin" encoding="base64" content="U0hFTEwgRU1VTEFUT1I="/>
    </vfs>

Атрибут encoding="base64" — для двоичных данных.

Команды:

| Команда | Описание |
|---------|----------|
| ls [PATH] | список файлов и папок |
| cd [PATH] | переход в каталог |
| du [PATH] | размер файла или каталога |
| wc FILE | число строк, слов и символов |
| echo TEXT... | вывод аргументов |
| touch FILE | создать пустой файл |
| chown USER FILE | сменить владельца (в памяти) |
| exit | закрыть окно |

## Сборка и запуск

Зависимостей нет — только стандартная библиотека Python 3.10+.

Запуск:

    run.bat

Или напрямую:

    python -m src.main --vfs test_data/medium.xml --script scripts/test_stage5.emu

Запуск тестов:

    python -m pytest tests/ -v

## Примеры использования

С VFS и скриптом:

    python -m src.main --vfs test_data/deep.xml --script scripts/test_stage4.emu

Только с VFS:

    python -m src.main --vfs test_data/minimal.xml

Пример сеанса в GUI:

    > ls
    docs
    encoded.bin
    file1.txt
    file2.txt
    > cd docs
    > ls
    doc1.txt
    > cd ..
    > wc file1.txt
    0318file1.txt
    > touch new_file.txt
    > chown admin file1.txt
    > exit

## Структура репозитория

    .
    ├── README.md
    ├── .gitignore
    ├── run.bat
    ├── requirements.txt
    ├── src/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── gui.py
    │   ├── parser.py
    │   ├── config.py
    │   ├── script_runner.py
    │   ├── vfs.py
    │   └── commands.py
    ├── tests/
    │   └── test_emulator.py
    ├── scripts/
    │   ├── test_minimal.emu
    │   ├── test_no_exit.emu
    │   ├── test_stage4.emu
    │   └── test_stage5.emu
    └── test_data/
        ├── minimal.xml
        ├── medium.xml
        └── deep.xml