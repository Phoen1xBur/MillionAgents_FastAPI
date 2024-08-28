from datetime import datetime
from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column, JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class File(Base):
    __tablename__ = 'file'
    
    id = Column('id', Integer, primary_key=True, index=True)
    path_filename = Column('path_filename', String, nullable=False)
    original_name = Column('original_name', String, nullable=False)
    format = Column('format', String, nullable=False)
    extension = Column('extension', String, nullable=False)
    size = Column('size', Integer, nullable=False)
    created_at = Column('created_at', TIMESTAMP, default=datetime.utcnow)
