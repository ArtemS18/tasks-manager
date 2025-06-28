import typing
from .template import hello_template
from .connect import client

if typing.TYPE_CHECKING:
    from app.web.app import FastAPI

async def send_email(app: "FastAPI", user_id: int):
    user = await app.store.user.get_user_by_id(user_id)

    msg = hello_template(
        from_email="root@localhost", 
        to_email=user.login
    )

    async with client:
        await client.send_message(msg)
