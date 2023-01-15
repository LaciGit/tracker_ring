from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

import json
import unittest

import pandas as pd

from tracker.db.db import DatabaseJSON
from tracker.db.db.preset import PRESET_TEST
from tracker.models import Area, Tag, Task, Topic, DataBaseSchema
from tracker.models.database_schema_json import DBBase


class TestDatabaseJSON(unittest.TestCase):

    test_path = "./data/db/test_db.json"

    def test__init__empty(self):
        test_db = DatabaseJSON("./data/db/test_db_new_when_empty.json")
        self.assertTrue(isinstance(test_db._db, DataBaseSchema))

    def test__init__empty_with_preset(self):
        test_db = DatabaseJSON("./data/db/test_db.json", preset=PRESET_TEST)
        self.assertTrue(isinstance(test_db._db, DataBaseSchema))

    def test__init__existing(self):
        test_db = DatabaseJSON("./data/db/test_db.json")
        self.assertTrue(isinstance(test_db._db, DataBaseSchema))

    def test__post_duplicate(self) -> None:
        test_db = DatabaseJSON("./data/db/test_db.json")
        area = Area(name="dup")
        test_db.post(area)
        with self.assertRaises(LookupError):
            test_db.post(area)

    def test__get_exceptions(self) -> None:
        test_db = DatabaseJSON("./data/db/test_db.json")

        with self.assertRaises(LookupError):
            test_db.get(cls="not an cls", id="not an id")

        with self.assertRaises(LookupError):
            test_db.get(cls=Area.__name__, id="not an id")

    def test__write_sample(self) -> None:
        path_test_write = Path("./data/db/test_write.json").resolve()
        path_test_write.unlink(missing_ok=True)

        test_db = DatabaseJSON(path_test_write, preset=PRESET_TEST)

        test_db.save()

    def test__get_area(self) -> None:
        test_db = DatabaseJSON(self.test_path)
        area = test_db.get(cls=Area.__name__, id="aebb97c9-0947-4a89-a30b-37947d9074c9")

        self.assertFalse(isinstance(area, Dict))
        self.assertEqual(area.name, "Work")

    def test__get_area_by_name(self) -> None:
        test_db = DatabaseJSON(self.test_path)
        area = test_db.get(cls=Area.__name__, name="Work")

        self.assertFalse(isinstance(area, Dict))
        self.assertEqual(area.name, "Work")

    def test__get_df(self) -> None:
        test_db = DatabaseJSON(self.test_path)
        df = test_db.get_df()

        self.assertTrue(isinstance(df, pd.DataFrame))

    def test__get_unique(self) -> None:
        test_db = DatabaseJSON(self.test_path)
        areas = test_db.get_unique(cls="area")

        self.assertIn("aebb97c9-0947-4a89-a30b-37947d9074c9", areas)
        self.assertIn("13a87fed-152e-4cf3-8657-ea622a0a37a6", areas)

    def test__update(self) -> None:
        test_db = DatabaseJSON(self.test_path)

        area = test_db.get(cls=Area.__name__, id="aebb97c9-0947-4a89-a30b-37947d9074c9")

        topic = Topic(name="new_topic")
        test_db.post(topic)

        test_db.update_by_child(parent=area, child=topic)
        t = test_db.get(cls=Topic.__name__, id=topic.id)

        self.assertTrue(isinstance(t, Topic))
