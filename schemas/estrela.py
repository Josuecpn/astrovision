from pydantic import BaseModel
from typing import Optional

# Gabarito para criar uma estrela (POST)
class EstrelaCreate(BaseModel):
    nome: str
    codigo_estelar: Optional[str] = None
    tipo_espectral: str
    massa: float
    temperatura: int
    idade_bilhoes_anos: float

# Gabarito para responder os dados da estrela (Response)
class Estrela(EstrelaCreate):
    id: int

    class Config:
        from_attributes = True
