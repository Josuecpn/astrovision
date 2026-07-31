from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
import services.planet_service as planet_service
from db import get_db

router = APIRouter(prefix="/planetas", tags=["Planetas"])

@router.post("/", response_model=schemas.Planeta, status_code=status.HTTP_201_CREATED)
def cadastrar_planeta(planeta_in: schemas.PlanetaCreate, db: Session = Depends(get_db)):
    return planet_service.criar_planeta(db, planeta_in)

@router.get("/", response_model=list[schemas.Planeta])
def buscar_todos(db: Session = Depends(get_db)):
    return planet_service.listar_planetas(db)

@router.put("/{planeta_id}", response_model=schemas.Planeta)
def modificar_planeta(planeta_id: int, planeta_in: schemas.PlanetaCreate, db: Session = Depends(get_db)):
    return planet_service.atualizar_planeta(db, planeta_id, planeta_in)

@router.delete("/{planeta_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_planeta(planeta_id: int, db: Session = Depends(get_db)):
    planet_service.deletar_planeta(db, planeta_id)
    return None
