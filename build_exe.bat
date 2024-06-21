pyinstaller --noconfirm --onefile --console --icon "C:/Users/joe/repos/babel/babel.ico"  "C:/Users/joe/repos/babel/babel.py"

:: Copy the specified directories
xcopy "books" "dist\books" /E /I /Y
xcopy "data" "dist\data" /E /I /Y

:: Copy the specified files
copy "pack.png" "dist\pack.png" /Y
copy "config*.yaml" "dist\" /Y
copy "README.md" "dist\README.md" /Y
copy "LICENSE.txt" "dist\LICENSE.txt" /Y
