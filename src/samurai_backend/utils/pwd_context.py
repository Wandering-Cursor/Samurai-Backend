from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    argon2__rounds=8,
    argon2__memory_cost=32 * 1024,  # 32MB
    argon2__parallelism=1,
)
