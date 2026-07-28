from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.db_connection import Base

class Planeta(Base):
    __tablename__ = "planetas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    tipo = Column(String)
    raio_km = Column(Float)
    habitavel = Column(Integer)
    periodo_orbital_dias = Column(Float)

    estrela_id = Column(Integer, ForeignKey("estrelas.id"), nullable=True)

    estrela = relationship("Estrela", back_populates="planetas")
    meteoros = relationship("Meteoro", back_populates="planeta")
