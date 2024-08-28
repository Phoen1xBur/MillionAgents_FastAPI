from pydantic import BaseModel, Field


class SFile(BaseModel):
    # name: Field(alias='original_name')
    id: int
    original_name: str
    format: str
    extension: str
    size: int

