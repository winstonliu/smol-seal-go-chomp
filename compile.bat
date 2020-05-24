@echo off
pyinstaller --icon=assets\seal.ico -w -n smol_seal_go_chomp main.py
timeout /t 5
xcopy FreeSansBold.ttf dist\smol_seal_go_chomp\
xcopy /e assets dist\smol_seal_go_chomp\assets\
