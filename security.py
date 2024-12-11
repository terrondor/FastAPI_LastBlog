from passlib.context import CryptContext

   # Создаем экземпляр CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

   # Функция для хеширования пароля
def hash_password(password: str):
       return pwd_context.hash(password)

   # Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str):
       return pwd_context.verify(plain_password, hashed_password)