from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.projects import router as projects_router
from app.api.sites import router as sites_router
from app.api.metrics import router as metrics_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(sites_router)
app.include_router(metrics_router)


@app.on_event("startup")
def auto_seed_demo_data():
    try:
        from app.seed_full_demo import seed_full_demo
        seed_full_demo()
    except Exception as e:
        print(f"Auto-seed notification: {e}")


