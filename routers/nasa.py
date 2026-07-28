from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import services.nasa_service as nasa_service
from db import get_db

router = APIRouter(prefix="/data-ingestion", tags=["Carga de Dados (NASA)"])

@router.post("/fetch-exoplanets", status_code=status.HTTP_200_OK)
def buscar_dados_da_nasa(db: Session = Depends(get_db)):
    """
    Consome os dados reais do arquivo da NASA, faz a limpeza/conversão física 
    dos raios planetários e injeta direto no banco de dados local.
    """
    return nasa_service.popular_banco_com_dados_nasa(db)
