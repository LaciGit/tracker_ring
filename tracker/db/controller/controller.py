import numpy as np
import pandas as pd

from datetime import datetime
from functools import cache
from typing import List, Optional, Tuple


from enum import Enum, auto

from tracker import SETTINGS
from tracker.db.db import Database, DatabaseJSON
from tracker.db.db.preset import presets
from tracker.models import DBBase


class Controller:
    def __init__(self, db_type: Optional[str] = None) -> None:
        if db_type:
            self._db_type = db_type
        else:
            self._db_type = SETTINGS.db.type

        self._db: Database = self._init_db()

    def _init_db(self) -> Database:
        if self._db_type == "json":
            return DatabaseJSON(
                path_to_json=SETTINGS.db.path,
                preset=presets.get(SETTINGS.db.preset),
            )
        else:
            raise NotImplementedError("DB type not implemented!")

    def get(self, cls: str, id: Optional[str] = None, name: Optional[str] = None) -> DBBase:
        return self._db.get(cls, id, name)

    def post(self, *objects: DBBase) -> None:
        self._db.post(*objects)

    def get_df(self, clean_ids: Optional[bool] = False) -> pd.DataFrame:
        if clean_ids:
            df = self._db.get_df()
            df = df.drop(columns=[c for c in df.columns if "id" in c])
            return df
        return self._db.get_df()

    # @cache
    def get_unique(self, cls: str, as_name: Optional[bool] = True) -> List[str]:
        """get unique either by id or name

        Args:
            cls (str): db class name
            as_name (Optional[bool], optional): id or name of dbbase. Defaults to True.

        Returns:
            List[str]: ids or names
        """
        ids = self._db.get_unique(cls)
        if not as_name:
            return list(set(ids))

        return set([self.get(cls=cls, id=id).name for id in ids])

    def get_time_range(self) -> Tuple[datetime]:
        df = self.get_df(clean_ids=True)
        return (df.time.min(), df.time.max())

    def save(self) -> None:
        self._db.save()
