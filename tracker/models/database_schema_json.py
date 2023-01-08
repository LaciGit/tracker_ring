from typing import Dict, List, Optional
from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class DBBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    child: Optional[str] = ""

    def __hash__(self):
        return hash(self.id)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.name}"


class Tag(DBBase):
    pass


class Task(DBBase):
    duration: int
    time: datetime
    tags: Optional[List[str]] = []
    child: str = Field(default="Tag")


class Topic(DBBase):
    bookingNumber: Optional[str] = ""
    tasks: Optional[List[str]] = []
    child: str = Field(default="Task")


class Area(DBBase):
    topics: Optional[List[str]] = []
    child: str = Field(default="Topic")


class DataBaseSchema(BaseModel):
    areas: Optional[Dict[str, Area]] = {}
    topics: Optional[Dict[str, Topic]] = {}
    tasks: Optional[Dict[str, Task]] = {}
    tags: Optional[Dict[str, Tag]] = {}
