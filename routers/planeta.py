from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
import services.planeta_service as planeta_service
from db import get_db

router = APIRouter(prefix="/planetas", tags=["Planetas"])

@router.post("/", response_model=schemas.Planeta, status_code=status.HTTP_201_CREATED)
def cadastrar_planeta(planeta_in: schemas.PlanetaCreate, db: Session = Depends(get_db)):
    return planeta_service.criar_planeta(db, planeta_in)

@router.get("/", response_model=list[schemas.Planeta])
def buscar_todos(db: Session = Depends(get_db)):
    return planeta_service.listar_planetas(db)
