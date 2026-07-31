from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.db_connection import Base

class Meteoro(Base):
    __tablename__ = "meteoros"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    composicao = Column(String)
    velocidade_km_s = Column(Float)
    massa_kg = Column(Float)
    tamanho_metros = Column(Float)

    estrela_id = Column(Integer, ForeignKey("estrelas.id"), nullable=True)
    planeta_id = Column(Integer, ForeignKey("planetas.id"), nullable=True)

    estrela = relationship("Estrela", back_populates="meteoros")
    planeta = relationship("Planeta", back_populates="meteoros")
