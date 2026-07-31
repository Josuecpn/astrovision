from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
import services.meteor_service as meteor_service
from db import get_db

router = APIRouter(prefix="/meteoros", tags=["Meteoros"])

@router.post("/", response_model=schemas.Meteoro, status_code=status.HTTP_201_CREATED)
def cadastrar_meteoro(meteoro_in: schemas.MeteoroCreate, db: Session = Depends(get_db)):
    return meteor_service.criar_meteoro(db, meteoro_in)

@router.get("/", response_model=list[schemas.Meteoro])
def buscar_todos(db: Session = Depends(get_db)):
    return meteor_service.listar_meteoros(db)

@router.put("/{meteoro_id}", response_model=schemas.Meteoro)
def modificar_meteoro(meteoro_id: int, meteoro_in: schemas.MeteoroCreate, db: Session = Depends(get_db)):
    return meteor_service.atualizar_meteoro(db, meteoro_id, meteoro_in)

@router.delete("/{meteoro_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_meteoro(meteoro_id: int, db: Session = Depends(get_db)):
    meteor_service.deletar_meteoro(db, meteoro_id)
    return None
