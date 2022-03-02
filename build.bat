pyinstaller cli.py --name pc_spec --windowed --clean --noconfirm --log-level DEBUG
copy %VIRTUAL_ENV%\share\sdl2\bin\libpng16-16.dll dist\pc_spec
tar.exe -c -v -f dist\pc_spec.zip dist\pc_spec