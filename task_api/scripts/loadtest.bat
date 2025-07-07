@echo off
call .venv\Scripts\activate
locust -f tests/locust/locustfile.py --host http://localhost:8080
pause