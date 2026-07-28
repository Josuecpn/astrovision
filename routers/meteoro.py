from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
import services.meteoro_service as meteoro_service
from db import get_db

router = APIRouter(prefix="/meteoros", tags=["Meteoros"])

@router.post("/", response_model=schemas.Meteoro, status_code=status.HTTP_201_CREATED)
def cadastrar_meteoro(meteoro_in: schemas.MeteoroCreate, db: Session = Depends(get_db)):
    return meteoro_service.criar_meteoro(db, meteoro_in)

@router.get("/", response_model=list[schemas.Meteoro])
def buscar_todos(db: Session = Depends(get_db)):
    return meteoro_service.listar_meteoros(db)
