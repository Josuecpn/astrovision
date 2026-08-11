from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
import models
from db import engine, get_db, Base
import routers

# Inicialize all tables in SQLite (dbastro.db) if they do not exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AstroVision",
    description="Astronomy API for managing celestial objects and events.",
    version="1.0.0",
    docs_url=None,
)

# Add routers to the API
app.include_router(routers.star_router)
app.include_router(routers.planet_router)
app.include_router(routers.meteor_router)
app.include_router(routers.nasa_router)
app.include_router(routers.analytics_router)
app.include_router(routers.physics_router)


@app.get("/")
def index():
    return {"status": "Sistema Operacional", "docs": "/docs"}

@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Docs",
    )
