@echo off
call .venv\Scripts\activate

IF "%~1" == "" (
    SET ARG=1
) ELSE (
    SET ARG=%~1
)


taskiq worker app.broker:broker --workers %ARG% --no-configure-logging --fs-discover
pause