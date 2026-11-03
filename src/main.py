"""Точка входа эмулятора."""
import argparse

from .gui import EmulatorGUI
from .script_runner import run_script
from .vfs import VFS


def main():
    parser = argparse.ArgumentParser(description="Эмулятор командной оболочки ОС")
    parser.add_argument("--vfs", type=str, help="Путь к XML-файлу VFS")
    parser.add_argument("--script", type=str, help="Путь к стартовому скрипту")
    args = parser.parse_args()

    print(f"DEBUG: Запуск эмулятора")
    print(f"DEBUG: VFS path = {args.vfs}")
    print(f"DEBUG: Script path = {args.script}")

    vfs = VFS()
    if args.vfs:
        try:
            vfs.load_from_xml(args.vfs)
            print(f"DEBUG: VFS успешно загружена из {args.vfs}")
        except FileNotFoundError:
            print(f"ОШИБКА: Файл VFS не найден: {args.vfs}")
            return
        except Exception as e:
            print(f"ОШИБКА при загрузке VFS: {e}")
            return

    if args.script:
        run_script(vfs, args.script)
        return

    app = EmulatorGUI(vfs)
    app.run()


if __name__ == "__main__":
    main()