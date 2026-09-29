"""Точка входа эмулятора оболочки."""
from src.config import debug_dump, parse_args
from src.gui import ShellGUI


def main() -> None:
    """Запускает GUI эмулятора с учётом параметров."""
    cfg = parse_args()
    gui = ShellGUI()
    gui.write(debug_dump(cfg))
    if cfg.vfs:
        gui.set_vfs(cfg.vfs)
    if cfg.script:
        gui.run_script_file(cfg.script)
    gui.run()


if __name__ == "__main__":
    main()
