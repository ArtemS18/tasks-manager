import bcrypt

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
