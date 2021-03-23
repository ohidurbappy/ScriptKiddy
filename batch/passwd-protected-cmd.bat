@echo off
:home
title Log in to CMD
color 07
cls
echo.
echo Cmd Accounts
echo =============
echo.
echo [1] Log In
echo [2] Sign Up
echo [3] Exit
echo.
set /p op=
if %op%==1 goto 1
if %op%==2 goto 2
if %op%==3 goto 3
goto error
:2
cls
echo Sign Up
echo ======================================
echo.
set /p newname="Enter new username:"
if "%newname%"=="%newname%" goto inputname
:inputname
cd "%userprofile%\documents"
if exist "cmdacoBin" goto skip
if not exist "cmdacoBin" goto noskip
:noskip
md "cmdacoBin"
goto skip
:skip
cd "%userprofile%\documents\cmdacoBin"
if exist "%newname%.bat" goto namexist
if not exist "%newname%.bat" goto skip2
:skip2
echo set realusername=%newname%> "%newname%.bat"
goto next
:next
echo.
set /p pswd=Enter new Password:
if "%pswd%"=="%pswd%" goto inputpass
:inputpass
cd "%userprofile%\documents\cmdacoBin"
echo set password=%pswd%>> "%newname%.bat"
goto next1
:namexist
echo.
echo The entered username already exists.
echo Press any key to return. . .
pause >nul
goto 2
:next1
cls
echo Cmd Accounts
echo ============
echo.
echo Your account has been successfully created!
echo.
pause
goto home
:1
color 07
cls
echo Cmd Accounts Log In
echo ================================
echo.
Set /p logname=Username:
if "%logname%"=="%logname%" goto 2.1
:2.1
echo.
set /p logpass="Password:"
if "%logpass%"=="%logpass%" goto login
:login
cd "%userprofile%\documents\cmdacoBin"
if exist "%logname%.bat" goto call
if not exist "%logname%.bat" goto errorlog
:call
call "%logname%.bat"
if "%password%"=="%logpass%" goto logdone
goto errorlog
:errorlog
color 0c
echo.
echo Username or Password incorrect.
echo Access denied.
pause >nul
goto home
:logdone
cls
echo Command Prompt
echo ==============
echo.
echo Successfully logged in!
echo.
pause
goto account
:account
cls
cd "%userprofile%\documents\cmdacoBin"
call "%realusername%color.bat"
call "%realusername%.bat"
color %colorcode%
cls
echo.
echo -------------------------------------------------------------------------------
echo %realusername%
echo -------------------------------------------------------------------------------
@echo off
break off
Title Command Prompt
color 0a
cls

echo Type "home" any time to go to the current user profile directory.
echo Type "desktop" any time to go to the current user desktop.
echo.
echo Type help to see list of common commands like cd, rd, md, del,
echo ren, replace, copy, xcopy, move, attrib, tree, edit, and cls.
echo Type [command]/? for detailed info.
echo.
pause
cls

:cmd
echo Directory: %CD%
set /P CMD=Command:
if "%CMD%" == "cls" goto cls
if "%CMD%" == "home" goto home2
if "%CMD%" == "desktop" goto desktop
if "%CMD%" == "red" goto red
if "%CMD%" == "green" goto green
if "%CMD%" == "normal" goto normal

%CMD%
cd C:\
goto cmd

:cls
cls
goto cmd

:home2
cd /d %USERPROFILE%
cls
goto cmd

:desktop
cd /d %SystemDrive%\Users\%USERNAME%\Desktop
cls
goto cmd

:red
color 0c
cls
goto cmd

:green
color 0a
cls
goto cmd

:normal
color 07
cls
goto cmd