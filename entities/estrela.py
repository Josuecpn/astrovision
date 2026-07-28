from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db.db_connection import Base

class Estrela(Base):
    __tablename__ = "estrelas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    tipo_espectral = Column(String)
    massa = Column(Float)
    temperatura = Column(Integer)
    idade_bilhoes_anos = Column(Float)

    # Usamos strings para referenciar classes em outros arquivos e evitar importação circular
    planetas = relationship("Planeta", back_populates="estrela")
    meteoros = relationship("Meteoro", back_populates="estrela")