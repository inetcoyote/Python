@echo off
rmdir /s /q build dist app.spec 2>nul
python -m PyInstaller --onefile --windowed --name=PyFormApp.exe app.py
pause