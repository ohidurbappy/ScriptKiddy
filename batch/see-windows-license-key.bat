@echo off
wmic path softwarelicensingservice get OA3xOriginalProductKey
set /p x="Press any key to continue..."