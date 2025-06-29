import typing
from .template import autho_email_template, hello_template
from .connect import client

if typing.TYPE_CHECKING:
    from app.web.app import FastAPI

async def send_hello_email(app: "FastAPI", user_id: int):
    user = await app.store.user.get_user_by_id(user_id)

    msg = hello_template(
        from_email="root@localhost", 
        to_email=user.login
    )

    async with client:
        await client.send_message(msg)

async def send_autho_email(app: "FastAPI", user_id: int):
    user = await app.store.user.get_user_by_id(user_id)
    password = await app.store.redis.get_confirming_password(user_id)

    if password is None:
        return

    msg = autho_email_template(
        from_email="root@localhost", 
        to_email=user.login,
        password=password
    )
    async with client:
        await client.send_message(msg)