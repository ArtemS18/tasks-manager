@echo off
call .venv\Scripts\activate
alembic revision --autogenerate -m "%~1"