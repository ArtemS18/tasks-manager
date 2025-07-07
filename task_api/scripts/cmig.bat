@echo off
call .venv\Scripts\activate
alembic revision --autogeberate -m "%~1"