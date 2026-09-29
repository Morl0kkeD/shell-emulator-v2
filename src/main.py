"""Точка входа эмулятора оболочки."""
from src.gui import ShellGUI


def main() -> None:
    """Запускает GUI эмулятора."""
    ShellGUI().run()


if __name__ == "__main__":
    main()
