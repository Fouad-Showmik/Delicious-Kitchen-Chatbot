from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    llm_base_url : str
    llm_api_key : str
    model_name : str

    system_prompt_file : str = "prompts/delicious_kitchen.md"
    max_history_messages : int
    session_ttl_seconds : int

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def system_prompt(self):
        return Path(self.system_prompt_file).read_text(encoding="utf-8")

settings = Settings()