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
        self.SECRET_KEY: str = os.getenv("SECRET_KEY")
        self.ALGORITHM: str = 'HS256'
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

        self.aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region: str = os.getenv("AWS_REGION")
        self.aws_bucket_name: str = os.getenv("AWS_BUCKET_NAME")


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
