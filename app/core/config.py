import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("BASE_DIR", BASE_DIR)

class Config:
    """
    기본 Configuration Class
    """
    def __init__(self):
        # DB 환경변수
        self.DATABASE_URL: str = os.getenv("DATABASE_URL")
        self.SECRET_CODE: str = os.getenv("SECRET_CODE")



class LocalConfig(Config):
    """
    로컬 환경 Configuration
    """
    def __init__(self):
        super().__init__()
        self.PROJECT_RELOAD: bool = True
        self.DATABASE_ECHO: bool = True
        self.LOG_LEVEL: str = "DEBUG"


class DevConfig(Config):
    """
    개발 환경 Configuration
    """
    def __init__(self):
        super().__init__()
        self.PROJECT_RELOAD: bool = True
        self.DATABASE_ECHO: bool = True
        self.LOG_LEVEL: str = "INFO"


class ProdConfig(Config):
    """
    운영 환경 Configuration
    """
    def __init__(self):
        super().__init__()
        self.PROJECT_RELOAD: bool = False
        self.DATABASE_ECHO: bool = False
        self.LOG_LEVEL: str = "WARNING"


def get_config(env):
    if env == "LOCAL":
        load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env.local'))
        return LocalConfig()

    elif env == "DEV":
        return DevConfig()

    elif env == "PROD":
        load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))
        return ProdConfig()

    else:
        raise ValueError(f"Invalid environment: {env}")


# 실행 환경 체크 후 config setting
env = os.getenv("ENV", "LOCAL")

print("env", env)
settings = get_config(env)
