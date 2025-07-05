import bcrypt
from random import choice
import asyncio

async def hash_password_async(password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    hashed = await asyncio.to_thread(bcrypt.hashpw, password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def hash_password(password: str):
    byte_password = password.encode()
    hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
    return hashed_password.decode()

def verify_password(password:str, hash_password: str):
    byte_password = password.encode()
    byte_hash_password = hash_password.encode()
    try:
        return bcrypt.checkpw(byte_password, byte_hash_password)
    except ValueError as e:
        return False

def create_confirm_password(leght: int=6, letters=True):
    digits = '0123456789'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    password = ''
    chars = digits[:]
    if letters:
        chars+=uppercase

    for i in range(leght):
        password+=choice(chars)
    return password


