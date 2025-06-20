from app.bd.repository.user import UserRepository
from .template import hello_template
from .connect import get_client


class SmtpClient:
    def __init__(self, repository):
        self.repository: UserRepository = repository

    async def send_email(self, user_id: int):
        client = get_client()
        user = await self.repository.get_user_by_id(user_id)

        msg = hello_template(
            from_email="root@localhost", 
            to_email=user.login
        )

        async with client:
            await client.send_message(msg)
