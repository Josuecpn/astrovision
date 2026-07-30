from fastapi import FastAPI
import models
from db import engine, get_db, Base
import routers

# Inicializa as tabelas no SQLite (dbastro.db) caso não existam
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AstroVision",
    description="Sistema astronômico desacoplado e escalável"
)

# Acopla os controladores modulares
app.include_router(routers.estrela_router)
app.include_router(routers.planeta_router)
app.include_router(routers.meteoro_router)
app.include_router(routers.nasa_router)
app.include_router(routers.analytics_router)
app.include_router(routers.physics_router)


@app.get("/")
def index():
    return {"status": "Sistema Operacional", "docs": "/docs"}
