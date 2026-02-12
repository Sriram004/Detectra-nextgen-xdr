from fastapi import FastAPI
from apps.api.app.core.config import settings
from apps.api.app.routes import alerts, incidents, playbooks


app = FastAPI(title=settings.app_name)
app.include_router(alerts.router, prefix=settings.api_prefix)
app.include_router(incidents.router, prefix=settings.api_prefix)
app.include_router(playbooks.router, prefix=settings.api_prefix)


@app.get("/healthz")
def healthcheck() -> dict:
    return {"status": "ok", "service": settings.app_name}
