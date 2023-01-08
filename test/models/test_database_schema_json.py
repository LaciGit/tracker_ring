from datetime import datetime, timedelta
from typing import Dict
import unittest

from tracker.models import Area, Tag, Task, Topic, DataBaseSchema


class TestDatabaseSchemaJSON(unittest.TestCase):
    def setUp(self) -> None:
        self._db = DataBaseSchema()

        self._area_work = Area(name="work")
        self._area_private = Area(name="private")

        self._topic_platform = Topic(name="platform", bookingNumber="AFE1")
        self._topic_application = Topic(name="application", bookingNumber="DFE1")

        self._tasks_etl_1 = Task(name="etl", duration=30, time=datetime.now())
        self._tasks_etl_2 = Task(
            name="etl",
            duration=30,
            time=datetime.now() - timedelta(days=1),
        )
        self._tasks_etl_2 = Task(
            name="etl",
            duration=60,
            time=datetime.now() - timedelta(days=2),
        )

        self._tasks_support = Task(
            name="support",
            duration=30,
            time=datetime.now() - timedelta(days=1),
        )
        self._tasks_support = Task(
            name="support",
            duration=10,
            time=datetime.now() - timedelta(days=2),
        )

        self._tag_highlight = Tag(name="highlight")
        self._tag_pain = Tag(name="pain")

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test__area__simple(self) -> None:
        self._db.areas[self._area_work.id] = self._area_work
        self._db.areas[self._area_private.id] = self._area_private

        self.assertEqual("work", self._db.areas.get(self._area_work.id).name)

    def test__area__with_children(self) -> None:
        self._area_children = Area(
            name="children",
            topics=[self._topic_application.id, self._topic_platform.id],
        )

    def test__str__(self) -> None:
        self.assertEqual(str(self._area_work), "Area: work")

    def test__hash__(self) -> None:
        self.assertEqual(self._area_work.__hash__(), hash(self._area_work.id))
