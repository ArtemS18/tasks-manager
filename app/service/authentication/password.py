from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['argon2'])

def hash_password(password: str):
    return crypt_context.hash(password)

def verify_password(password:str, hash_password: str):
    return password == hash_password
    #return crypt_context.verify(password, hash_password)