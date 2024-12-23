@echo off

set ZIP_PATH="C:\Program Files\7-Zip\7z.exe"

if "%1"=="" (
    echo Please provide the version number
    echo Usage: %0 version_number_string - e.g. '1.0'
    exit /b 1
)


::
:: Build windows vesion
::
echo Making windows builder with pyinstaller...
pyinstaller --noconfirm --onefile --console --icon babel.ico babel.py
echo Copying additional files...
:: Copy required directories and files
xcopy "books" "dist\books" /E /I /Y
xcopy "data" "dist\data" /E /I /Y
copy "pack.png" "dist\pack.png" /Y
copy "config*.yaml" "dist\" /Y
copy "README.md" "dist\README.md" /Y
copy "LICENSE.txt" "dist\LICENSE.txt" /Y
:: Zip dist
echo Zipping windows builder
%ZIP_PATH% a -tzip "babel-builder-windows_v%1.zip" ".\dist\*"
echo Windows builder done.


::
:: Build python version
::
echo Zipping python builder
%ZIP_PATH% a -tzip "babel-builder-python_v%1.zip" "pack.png" "config*.yaml" "README.md" "LICENSE.txt" "books\*" "data\*" "*.py"
echo Python builder done.


::
:: Build all packs
::
setlocal enabledelayedexpansion
:: Find all files matching the pattern config*.yaml in the current directory
for %%f in (config*.yaml) do (
    python babel.py -a %%f
)
endlocal

echo:
echo ALL DONE!
