from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import entities
import schemas

def criar_meteoro(db: Session, meteoro_in: schemas.MeteoroCreate) -> entities.Meteoro:
    # Regra: Validar FK da Estrela se enviada
    if meteoro_in.estrela_id:
        if not db.query(entities.Estrela).filter(entities.Estrela.id == meteoro_in.estrela_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A estrela informada não existe.")
            
    # Regra: Validar FK do Planeta se enviada
    if meteoro_in.planeta_id:
        if not db.query(entities.Planeta).filter(entities.Planeta.id == meteoro_in.planeta_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="O planeta informado não existe.")

    novo_meteoro = entities.Meteoro(**meteoro_in.model_dump())
    db.add(novo_meteoro)
    db.commit()
    db.refresh(novo_meteoro)
    return novo_meteoro

def listar_meteoros(db: Session) -> list[entities.Meteoro]:
    return db.query(entities.Meteoro).all()
