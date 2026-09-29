@echo off
chcp 65001 > nul
echo === Running emulator with Stage 5 script ===
python -m src.main --vfs test_data/medium.xml --script scripts/test_stage5.emu

echo.
echo === Running emulator in GUI mode ===
python -m src.main --vfs test_data/medium.xml
pause
