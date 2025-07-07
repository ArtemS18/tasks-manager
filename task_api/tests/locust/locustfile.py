from random import randint
from locust import HttpUser, task, between
from uuid import uuid4


class APIUser(HttpUser):
    wait_time = between(1, 2)

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
