from pathlib import Path
from typing import Dict

import unittest

import pandas as pd

from tracker import SETTINGS
from tracker.models import Area
from tracker.db.controller.controller import Controller


class TestController(unittest.TestCase):
    def setUp(self) -> None:
        self._controller = Controller()
        return super().setUp()

    def tearDown(self) -> None:
        del self._controller
        return super().tearDown()

    def test__db_type_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            Controller(db_type="oh no")

    def test__save(self) -> None:
        self._controller.save()

    def test__get_area(self) -> None:
        area = self._controller.get(
            cls=Area.__name__,
            id="aebb97c9-0947-4a89-a30b-37947d9074c9",
        )

        self.assertFalse(isinstance(area, Dict))
        self.assertEqual(area.name, "Work")

    def test__post_area(self) -> None:
        sample = Area(name="hi")
        self._controller.post(sample)
        self.assertEqual(sample, self._controller.get(Area.__name__, sample.id))

        self._controller.delete(sample)

    def test__get_df(self):
        df = self._controller.get_df()
        self.assertTrue(isinstance(df, pd.DataFrame))

    def test__get_unique_as_names(self) -> None:
        areas = self._controller.get_unique(cls="area")

        self.assertIn("Work", areas)
        self.assertIn("Private", areas)

    def test__get_unique_as_ids(self) -> None:
        areas = self._controller.get_unique(cls="area", as_name=False)

        self.assertIn("aebb97c9-0947-4a89-a30b-37947d9074c9", areas)
        self.assertIn("13a87fed-152e-4cf3-8657-ea622a0a37a6", areas)
