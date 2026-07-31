from pydantic import BaseModel
from typing import Optional

class PlanetaCreate(BaseModel):
    nome: str
    tipo: str
    raio_km: float
    habitavel: int  # 1 para Sim, 0 para Não
    periodo_orbital_dias: float
    estrela_id: Optional[int] = None  # Planeta pode pertencer a uma estrela ou não

class Planeta(PlanetaCreate):
    id: int

    class Config:
        from_attributes = True
