from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import entities
import schemas

def criar_planeta(db: Session, planeta_in: schemas.PlanetaCreate) -> entities.Planeta:
    # Regra: Se informou uma Estrela_id, ela deve existir no banco
    if planeta_in.estrela_id:
        estrela_existe = db.query(entities.Estrela).filter(entities.Estrela.id == planeta_in.estrela_id).first()
        if not estrela_existe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="A estrela hospedeira informada não existe."
            )

    novo_planeta = entities.Planeta(**planeta_in.model_dump())
    db.add(novo_planeta)
    db.commit()
    db.refresh(novo_planeta)
    return novo_planeta

def listar_planetas(db: Session) -> list[entities.Planeta]:
    return db.query(entities.Planeta).all()
