from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration, loaded from environment variables (or a
    local .env file during development). Nothing else in the app should
    read os.environ directly -- everything funnels through here so we
    have one place that defines what config the app needs.
    """

    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()
