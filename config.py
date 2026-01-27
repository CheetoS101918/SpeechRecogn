from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    name: str         # Название базы данных
    host: str         # URL-адрес базы данных
    user: str         # Username пользователя базы данных
    password: str     # Пароль к базе данных
    port: int


    def get_database_url():
        return f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}'
    

@dataclass
class TgBot:
    token: str     
    hf_token: str
    admin_ids: int 


@dataclass
class Config:
    bot: TgBot
#    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
        bot=TgBot(
            token=env('TOKEN'),
            admin_ids=env('ADMIN_IDS'),
            hf_token=env('HF_TOKEN')
        )
    )
    #     db=DatabaseConfig(
    #         name=env('DB_NAME'),
    #         host=env('DB_HOST'),
    #         user=env('DB_USER'),
    #         password=env('DB_PASSWORD'),
    #         port=env('DB_PORT')
    #     )
    # )
