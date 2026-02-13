from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_dir: str = "models"
    spacy_model: str = "en_core_web_sm"

    class Config:
        env_file = ".env"


settings = Settings()
