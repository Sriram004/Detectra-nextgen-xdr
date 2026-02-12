from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Detectra NextGen XDR"
    api_prefix: str = "/api/v1"
    jwt_secret: str = "dev-secret"


settings = Settings()
