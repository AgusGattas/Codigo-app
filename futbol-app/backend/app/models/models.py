from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date

Base = declarative_base()

class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    activo = Column(Boolean, default=True)
    asistencias = relationship("Asistencia", back_populates="jugador")
    estadisticas = relationship("Estadistica", back_populates="jugador")

class Asistencia(Base):
    __tablename__ = "asistencias"

    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey("jugadores.id"))
    fecha = Column(Date)
    tipo = Column(Enum('ENTRENAMIENTO', 'PARTIDO', name='tipo_evento'))
    presente = Column(Boolean, default=True)
    
    jugador = relationship("Jugador", back_populates="asistencias")

class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, default=date.today)
    rival = Column(String, index=True)
    resultado_local = Column(Integer, nullable=True)
    resultado_visitante = Column(Integer, nullable=True)
    lugar = Column(String)
    tipo = Column(String)
    estadisticas = relationship("Estadistica", back_populates="partido")

class Estadistica(Base):
    __tablename__ = "estadisticas"

    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey("jugadores.id"))
    partido_id = Column(Integer, ForeignKey("partidos.id"))
    goles = Column(Integer, default=0)
    asistencias = Column(Integer, default=0)
    tarjetas_amarillas = Column(Integer, default=0)
    tarjetas_rojas = Column(Integer, default=0)
    minutos_jugados = Column(Integer, default=0)
    titular = Column(Boolean, default=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    jugador = relationship("Jugador", back_populates="estadisticas")
    partido = relationship("Partido", back_populates="estadisticas") 