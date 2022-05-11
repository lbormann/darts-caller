@echo off
PUSHD .
:startover
echo (%time%) App started.
call "win-exec.bat"
echo (%time%) WARNING: App closed or crashed, restarting.
goto startover