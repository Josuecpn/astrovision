from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
import services.estrela_service as estrela_service
from db import get_db

router = APIRouter(prefix="/estrelas", tags=["Estrelas"])

@router.post("/", response_model=schemas.Estrela, status_code=status.HTTP_201_CREATED)
def cadastrar_estrela(estrela_in: schemas.EstrelaCreate, db: Session = Depends(get_db)):
    return estrela_service.criar_estrela(db, estrela_in)

@router.get("/", response_model=list[schemas.Estrela])
def buscar_todas(db: Session = Depends(get_db)):
    return estrela_service.listar_estrelas(db)

@router.put("/{estrela_id}", response_model=schemas.Estrela)
def modificar_estrela(estrela_id: int, estrela_in: schemas.EstrelaCreate, db: Session = Depends(get_db)):
    return estrela_service.atualizar_estrela(db, estrela_id, estrela_in)

@router.delete("/{estrela_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_estrela(estrela_id: int, db: Session = Depends(get_db)):
    estrela_service.deletar_estrela(db, estrela_id)
    return None
