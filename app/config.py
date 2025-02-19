from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = 8000
    MODEL_NAME: str = "GroNLP/bert-base-dutch-cased"
    SPACY_MODEL: str = "nl_core_news_sm"
    HUNSPELL_DICTIONARY: str = "nl_NL"

settings = Settings()
