from pydantic import BaseModel
from typing import Optional

class MeteoroCreate(BaseModel):
    nome: str
    composicao: str
    velocidade_km_s: float
    massa_kg: float
    tamanho_metros: float
    estrela_id: Optional[int] = None   # Pode pertencer a uma estrela...
    planeta_id: Optional[int] = None   # ...a um planeta, ou nenhum dos dois.

class Meteoro(MeteoroCreate):
    id: int

    class Config:
        from_attributes = True
