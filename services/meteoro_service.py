from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import entities
import schemas

# POST
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

# GET
def listar_meteoros(db: Session) -> list[entities.Meteoro]:
    return db.query(entities.Meteoro).all()

# PUT
def atualizar_meteoro(db: Session, meteoro_id: int, meteoro_in: schemas.MeteoroCreate) -> entities.Meteoro:
    db_meteoro = db.query(entities.Meteoro).filter(entities.Meteoro.id == meteoro_id).first()
    if not db_meteoro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meteoro não encontrado.")

    # Regras: Validar novas FKs se enviadas
    if meteoro_in.estrela_id and not db.query(entities.Estrela).filter(entities.Estrela.id == meteoro_in.estrela_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A estrela informada não existe.")
        
    if meteoro_in.planeta_id and not db.query(entities.Planeta).filter(entities.Planeta.id == meteoro_in.planeta_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="O planeta informado não existe.")

    for chave, valor in meteoro_in.model_dump().items():
        setattr(db_meteoro, chave, valor)

    db.commit()
    db.refresh(db_meteoro)
    return db_meteoro

# DELETE
def deletar_meteoro(db: Session, meteoro_id: int) -> None:
    db_meteoro = db.query(entities.Meteoro).filter(entities.Meteoro.id == meteoro_id).first()
    if not db_meteoro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meteoro não encontrado.")

    # Meteoros não possuem dependentes na nossa modelagem, exclusão livre
    db.delete(db_meteoro)
    db.commit()
