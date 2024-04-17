from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_title: str = 'Puzzle game'
    connection_string: str = 'sqlite+aiosqlite://'
    max_cells: int = 120


settings = Settings()
