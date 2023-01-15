import json

from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID

import pandas as pd
from tracker.db.db.database import Database
from tracker.models import Area, Tag, Task, Topic, DataBaseSchema, DBBase


class DatabaseJSON(Database):
    def __init__(
        self,
        path_to_json: str,
        preset: Optional[DataBaseSchema] = None,
    ) -> None:
        super().__init__(preset)

        self._path = Path(path_to_json).resolve()

        try:
            with open(path_to_json) as json_file:
                data = DataBaseSchema(**json.load(json_file))
        except FileNotFoundError:
            if preset:
                data = preset
            else:
                data = DataBaseSchema()

        self._db = data
        super().__init__()

    def post(self, *objects: DBBase) -> None:
        for object in objects:
            attr_name = object.__class__.__name__.lower()

            attr = getattr(self._db, f"{attr_name}s")

            if attr.get(object.id):
                raise LookupError(f"'{attr_name}' already exists!")

            attr[object.id] = object

    def delete(self, *objects: DBBase) -> None:
        for object in objects:
            attr_name = object.__class__.__name__.lower()

            attr = getattr(self._db, f"{attr_name}s")

            if attr.get(object.id):
                del attr[object.id]

    def update_by_child(self, parent: DBBase, child: DBBase) -> None:
        # check if parent exists
        attr_name = parent.__class__.__name__.lower()
        attr = getattr(self._db, f"{attr_name}s")
        parent = attr.get(parent.id)
        if not parent:
            raise LookupError(f"'{attr_name}' does not exists!")

        # check if child exists
        child_attr_name = child.__class__.__name__.lower()
        child_attr = getattr(self._db, f"{child_attr_name}s")
        child = child_attr.get(child.id)
        if not child:
            raise LookupError(f"'{child_attr_name}' does not exists!")

        # update
        child_container = getattr(parent, f"{child_attr_name}s")
        child_container.append(child.id)

        attr[parent.id] = parent

    def get(
        self,
        cls: str,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> DBBase:
        try:
            attr = getattr(self._db, f"{cls.lower()}s")
        except:
            raise LookupError(f"cls: {cls} not in DBBase Model")

        if not id and not name:
            raise TypeError("Either id or name must no be 'None'.")

        if id:
            if object := attr.get(id):
                return object
            raise LookupError(f"Object of type '{cls}' with id '{id}' does not exists!")

        if name:
            for _, item in attr.items():
                if item.name == name:
                    return item

            raise LookupError(
                f"Object of type '{cls}' with name '{name}' does not exists!"
            )

    def get_unique(self, cls: str) -> List[str]:
        try:
            attr: Dict[str, Any] = getattr(self._db, f"{cls.lower()}s")
        except:
            raise LookupError(f"cls: {cls} not in DBBase Model")

        return list(attr.keys())

    def save(self) -> None:
        with open(self._path, "w+") as fp:
            json.dump(json.loads(self._db.json()), fp)

    def _recursive_build(
        self,
        parent_slice: Dict,
        child: DBBase,
    ) -> List[Dict[str, Any]]:

        result = []

        sub_child_attr_name = f"{child.child.lower()}s"

        child_slice = child.dict(exclude={sub_child_attr_name, "child"})
        child_slice[f"{child.__class__.__name__.lower()}_id"] = child_slice.pop("id")
        child_slice[f"{child.__class__.__name__.lower()}_name"] = child_slice.pop(
            "name"
        )

        new_parent_slice = {**parent_slice, **child_slice}

        sub_child_ids = getattr(child, sub_child_attr_name, None)
        if sub_child_ids:
            for sub_child_id in sub_child_ids:
                result += self._recursive_build(
                    parent_slice=new_parent_slice,
                    child=self.get(child.child, sub_child_id),
                )

        else:
            result.append(new_parent_slice)

        return result

    def get_df(self) -> pd.DataFrame:

        rows = []
        for area in self._db.areas.values():
            rows += self._recursive_build(parent_slice={}, child=area)

        df = pd.concat([pd.DataFrame(raw, index=[0]) for raw in rows])
        return df
