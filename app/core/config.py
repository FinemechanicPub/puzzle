from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_title: str = 'Puzzle game'
    connection_string: str = 'sqlite+aiosqlite://'
    max_cells: int = 120
    page_limit: int = 20
    max_page: int = 100
    default_color: int = 14531481


settings = Settings()
