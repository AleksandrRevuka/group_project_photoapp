import redis.asyncio
import cloudinary

from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


async def init_async_redis():
    return redis.asyncio.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
    )


def init_cloudinary():
    return cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

class Settings(BaseSettings):
    postgres_user: str = 'postgres'
    postgres_password: str = '567234'
    postgres_db: str = 'postgres'
    postgres_domain: str = 'localhost'
    postgres_port: int = 5432

    secret_key: str = '7bbb3508e2e129ae2a3eabafdc76f20dd3211ee5660409019f710e2ea3d99f7b'
    algorithm: str = 'HS256'

    mail_username: str = 'fastapi_kulyk@meta.ua'
    mail_password: str = 'pythonCourse2023'
    mail_from: str = 'fastapi_kulyk@meta.ua'
    mail_port: int = 465
    mail_server: str = 'smtp.meta.ua'

    redis_host: str = 'localhost'
    redis_port: int = 6379

    cloudinary_name: str = 'drb36q0vc'
    cloudinary_api_key: str = '681646296468926'
    cloudinary_api_secret: str = 'SoAcTSjL6c1ec7JGnBNv7hqIJgY'

    class ConfigDict:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def sqlalchemy_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_domain}/{self.postgres_db}"


settings = Settings()  # type: ignore
