from typing import List, Optional
import pandas as pd
from abc import ABC, abstractmethod
from tracker.models import Area, Tag, Task, Topic, DBBase, DataBaseSchema


class Database(ABC):
    @abstractmethod
    def __init__(
        self, preset: Optional[DataBaseSchema] = None
    ) -> None:  # pragma: no cover
        # how to connect to data/read
        pass

    @abstractmethod
    def post(self, *objects: DBBase) -> None:  # pragma: no cover
        pass

    @abstractmethod
    def get(
        self,
        cls: str,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> DBBase:  # pragma: no cover
        pass

    @abstractmethod
    def save(self) -> None:  # pragma: no cover
        pass

    @abstractmethod
    def get_df(self) -> pd.DataFrame:  # pragma: no cover
        pass

    @abstractmethod
    def get_unique(self, cls: str) -> List[str]:  # pragma: no cover
        pass
