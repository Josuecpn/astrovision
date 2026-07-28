from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import entities
import schemas

# POST
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

# GET
def listar_planetas(db: Session) -> list[entities.Planeta]:
    return db.query(entities.Planeta).all()

# PUT
def atualizar_planeta(db: Session, planeta_id: int, planeta_in: schemas.PlanetaCreate) -> entities.Planeta:
    db_planeta = db.query(entities.Planeta).filter(entities.Planeta.id == planeta_id).first()
    if not db_planeta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planeta não encontrado.")

    # Regra: Se alterou a estrela_id, valida se a nova estrela existe
    if planeta_in.estrela_id:
        estrela_existe = db.query(entities.Estrela).filter(entities.Estrela.id == planeta_in.estrela_id).first()
        if not estrela_existe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A estrela hospedeira informada não existe.")

    for chave, valor in planeta_in.model_dump().items():
        setattr(db_planeta, chave, valor)

    db.commit()
    db.refresh(db_planeta)
    return db_planeta

# DELETE
def deletar_planeta(db: Session, planeta_id: int) -> None:
    db_planeta = db.query(entities.Planeta).filter(entities.Planeta.id == planeta_id).first()
    if not db_planeta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planeta não encontrado.")
    
    # Regra de Segurança: Bloquear exclusão se houver meteoros associados
    if db_planeta.meteoros:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Não é possível deletar um planeta que possui meteoros associados."
        )

    db.delete(db_planeta)
    db.commit()
