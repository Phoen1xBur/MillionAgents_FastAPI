from datetime import datetime, UTC
from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column, JSON

metadata = MetaData()

file = Table(
    'file',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('path_filename', String, nullable=False),
    Column('name', String, nullable=False),
    Column('format', String, nullable=False),
    Column('extension', String, nullable=False),
    Column('size', Integer, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.now(UTC)),
)
