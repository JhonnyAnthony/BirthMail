from pydantic import BaseModel, Field
from typing import List
from enum import Enum
import sys

sys.path.append('C:/Github/BirthMail/src')
from connectionDB import Database

class Connection:
    def __init__(self):
        self.db = Database()
        self.db.connectData()

    def connection(self):
        return self.db.query()
class Category(str, Enum):
    DIRETOR = "diretor"
    SUPERVISOR = "supervisor"
    COORDENADOR = "coordenador"
    EMPLOYEE = "employee"

class Item(BaseModel):
    id: int
    nome: str
    data_nas: str
    cargo: str
    category: Category
class SubordinadoItem(BaseModel):
    id: int
    nome: str
    data_nas: str
    cargo: str
    idPos: int
    category: Category
    subordinados: List[Item] = Field(default_factory=list)

class CoordenadorItem(BaseModel):
    id: int
    nome: str
    data_nas: str
    cargo: str
    idPos: int
    category: Category
    subordinados: List[Item] = Field(default_factory=list)
class SupervisorItem(BaseModel):
    id: int
    nome: str
    data_nas: str
    cargo: str
    idPos: int
    category: Category
    coordenadores: List[CoordenadorItem] = Field(default_factory=list)

class DiretorItem(BaseModel):
    id: int
    nome: str
    data_nas: str
    cargo: str
    idPos: int
    category: Category
    supervisores: List[SupervisorItem] = Field(default_factory=list)