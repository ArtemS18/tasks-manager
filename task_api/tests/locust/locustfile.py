from random import randint
from locust import HttpUser, task, between
from uuid import uuid4


class APIUser(HttpUser):
    wait_time = between(0.1, 0.3)

    @task
    def reg_user(self):
        user_id = uuid4().hex
        tg_id = randint(10, 10**8 - 1)  # 9-значное число
        data = {
            "login": f"{user_id}@email.com",
            "password": "123456789",
            "tg_id": tg_id,
            "name": "test_user",
        }
        resp = self.client.post("/auth/reg", json=data)

    @task
    def get_tasks(self):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhcnRvMjNyMTEyMjFqQGdtYWlsLmNvbSIsImlkIjozMTU5NCwibmFtZSI6ImFydGVta2EiLCJleHAiOjE3NTIxOTQ0MjV9.1TYoW1K0YSDOTGsHEIGjxuD_yIj5enkdcKV00QCJN9E"
        self.client.get("/tasks/", headers={"Authorization": f"Bearer {token}"})
