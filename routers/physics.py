from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
import services.physics_service as physics_service
from db import get_db

router = APIRouter(prefix="/physics", tags=["Física Computacional"])

@router.get("/kepler-law/{planeta_id}")
def calcular_orbita_planeta(planeta_id: int, db: Session = Depends(get_db)):
    """
    Aplica a Terceira Lei de Kepler para calcular a distância média (Semieixo Maior) 
    de um exoplaneta até sua estrela hospedeira com base no período orbital real da NASA.
    """
    return physics_service.calcular_distancia_kepleriana(db, planeta_id)

@router.get("/kepler-law/{planeta_id}/view", response_class=HTMLResponse)
def visualizar_orbita_planeta(planeta_id: int, db: Session = Depends(get_db)):
    """
    Renderiza um mapa orbital interativo em HTML/Plotly aplicando as Leis de Kepler 
    para o exoplaneta selecionado. Funciona 100% offline.
    """
    return physics_service.gerar_visualizacao_orbita_kepler(db, planeta_id)