from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import models
import schemas

# POST
def criar_estrela(db: Session, estrela_in: schemas.EstrelaCreate) -> models.Estrela:
    # Regra: Não permitir nomes duplicados no universo
    db_estrela = db.query(models.Estrela).filter(models.Estrela.nome == estrela_in.nome).first()
    if db_estrela:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Uma estrela com esse nome já existe."
        )
    
    nova_estrela = models.Estrela(**estrela_in.model_dump())
    db.add(nova_estrela)
    db.commit()
    db.refresh(nova_estrela)
    return nova_estrela

# GET
def listar_estrelas(db: Session) -> list[models.Estrela]:
    return db.query(models.Estrela).all()

# PUT
def atualizar_estrela(db: Session, estrela_id: int, estrela_in: schemas.EstrelaCreate) -> models.Estrela:
    # 1. Busca a estrela existente
    db_estrela = db.query(models.Estrela).filter(models.Estrela.id == estrela_id).first()
    if not db_estrela:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estrela não encontrada.")
    
    # 2. Regra: Não permitir mudar o nome para um que já existe em OUTRA estrela
    nome_duplicado = db.query(models.Estrela).filter(
        models.Estrela.nome == estrela_in.nome, 
        models.Estrela.id != estrela_id
    ).first()
    if nome_duplicado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esse nome de estrela já está em uso.")

    # 3. Atualiza os campos dinamicamente
    for chave, valor in estrela_in.model_dump().items():
        setattr(db_estrela, chave, valor)

    db.commit()
    db.refresh(db_estrela)
    return db_estrela

# DELETE
def deletar_estrela(db: Session, estrela_id: int) -> None:
    db_estrela = db.query(models.Estrela).filter(models.Estrela.id == estrela_id).first()
    if not db_estrela:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estrela não encontrada.")
    
    # Regra de Segurança: Bloquear exclusão se houver dependências
    if db_estrela.planetas or db_estrela.meteoros:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Não é possível deletar uma estrela que possui planetas ou meteoros associados."
        )

    db.delete(db_estrela)
    db.commit()
