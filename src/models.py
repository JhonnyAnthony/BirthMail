from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Category(str, Enum):
    DIRETOR = "diretor"
    SUPERIOR = "superior"
    EMPLOYEE = "employee"

class Item(BaseModel):
    id: int
    nome: str
    data_nas: str
    cargo: str
    category: Category

class CoordenadorItem(BaseModel):
    id: int
    nome: str
    cargo: str
    data_nas: str
    category: Category
    subordinados: List[Item] = Field(default_factory=list)

class SupervisorItem(BaseModel):
    id: int
    nome: str
    cargo: str
    data_nas: str
    category: Category
    coordenadores: List[CoordenadorItem] = Field(default_factory=list)

class DiretorItem(BaseModel):
    id: int
    nome: str
    cargo: str
    data_nas: str
    category: Category
    supervisores: List[SupervisorItem] = Field(default_factory=list)