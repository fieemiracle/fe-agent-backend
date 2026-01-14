from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    应用配置类

    配置优先级（从高到低）：
    1. 系统环境变量（如 .zshrc 中配置的）
    2. .env 文件
    3. 代码中的默认值
    """

    APP_NAME: str = "FastAPI Starter"
    VERSION: str = "0.1.0"

    # OpenAI API Key - 从环境变量读取，不要在代码中硬编码
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
