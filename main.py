from fastapi import FastAPI
import entities
from db import engine
import routers

# Inicializa as tabelas no SQLite (dbastro.db) caso não existam
entities.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Cosmos - Arquitetura de Serviços",
    description="Sistema astronômico desacoplado e escalável"
)

# Acopla os controladores modulares
app.include_router(routers.estrela_router)
app.include_router(routers.planeta_router)
app.include_router(routers.meteoro_router)

@app.get("/")
def index():
    return {"status": "Sistema Operacional", "docs": "/docs"}
