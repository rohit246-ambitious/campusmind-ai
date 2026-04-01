from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(password, hashed)
