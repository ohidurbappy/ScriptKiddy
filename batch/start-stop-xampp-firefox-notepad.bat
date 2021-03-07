@echo off
tasklist /FI "IMAGENAME eq xampp-control.exe" | findstr /I "xampp-control.exe" && (
    taskkill /IM firefox.exe
    taskkill /IM notepad++.exe
    cd "C:\xampp"
    call apache_stop.bat
    call mysql_stop.bat
    taskkill /f /IM xampp-control.exe
) || (
    start C:\xampp\xampp-control.exe
    cd "C:\Program Files\Notepad++"
    start notepad++.exe
    cd "C:\Program Files\Mozilla Firefox"
    start firefox.exe http://localhost/
)
exit
