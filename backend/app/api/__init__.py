from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.projects import router as projects_router
from app.api.sites import router as sites_router
from app.api.metrics import router as metrics_router

__all__ = ["health_router", "auth_router", "projects_router", "sites_router", "metrics_router"]
