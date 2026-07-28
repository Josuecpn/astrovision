from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import entities
import schemas

def criar_estrela(db: Session, estrela_in: schemas.EstrelaCreate) -> entities.Estrela:
    # Regra: Não permitir nomes duplicados no universo
    db_estrela = db.query(entities.Estrela).filter(entities.Estrela.nome == estrela_in.nome).first()
    if db_estrela:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Uma estrela com esse nome já existe."
        )
    
    nova_estrela = entities.Estrela(**estrela_in.model_dump())
    db.add(nova_estrela)
    db.commit()
    db.refresh(nova_estrela)
    return nova_estrela

def listar_estrelas(db: Session) -> list[entities.Estrela]:
    return db.query(entities.Estrela).all()
