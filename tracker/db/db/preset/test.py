from datetime import datetime, timedelta
from tracker.models import DataBaseSchema, Area, Tag, Task, Topic

# Tags

firefighting = Tag(name="Firefighting")
ok = Tag(name="OK")
highlight = Tag(name="Highlight")
pain = Tag(name="Pain")

list_tags = [firefighting, ok, highlight, pain]

# Tasks
tasks_strech = [
    Task(
        name="Strech",
        duration=10,
        time=datetime.now() - timedelta(days=i),
    )
    for i in range(20)
]
tasks_sit_ups = [
    Task(
        name="Sit-up",
        duration=3,
        time=datetime.now() - timedelta(days=2 * i),
    )
    for i in range(20)
]
tasks_pull_ups = [
    Task(
        name="Pull-ups",
        duration=5,
        time=datetime.now() - timedelta(days=2 * i),
    )
    for i in range(20)
]
tasks_push_ups = [
    Task(
        name="Push-ups",
        duration=2,
        time=datetime.now() - timedelta(days=2 * i),
    )
    for i in range(20)
]

tasks_elden_ring = [
    Task(
        name="EldenRing",
        duration=180,
        time=datetime.now() - timedelta(days=7 * i),
    )
    for i in range(20)
]
tasks_civ = [
    Task(
        name="Civilization 6",
        duration=240,
        time=datetime.now() - timedelta(days=6 * i),
    )
    for i in range(20)
]

tasks_platform = []
for i in range(100):
    if i not in [0, 6, 7]:
        if i % 2 == 0:
            name = "Components"
            duration = 120
            t_tags = [ok.id]
        else:
            name = "FaserProcessing"
            duration = 120
            t_tags = [ok.id]

        if i % 11 == 0:
            name = "Innovation"
            duration = 480
            t_tags = [highlight.id]

        task = Task(
            name=name,
            duration=duration,
            time=datetime.now() - timedelta(days=i),
            tags=t_tags,
        )
        tasks_platform.append(task)

tasks_project_1 = []
for i in range(100):
    if i not in [0, 6, 7]:
        if i % 2 == 0:
            name = "Support"
            duration = 15
            t_tags = [pain.id]
        else:
            name = "Operation"
            duration = 60
            t_tags = [ok.id]

        if i % 17 == 0:
            name = "Analytics"
            duration = 240
            t_tags = [ok.id]

        task = Task(
            name=name,
            duration=duration,
            time=datetime.now() - timedelta(days=i),
            tags=t_tags,
        )
        tasks_project_1.append(task)

tasks_project_2 = []
for i in range(100):
    if i not in [0, 6, 7]:
        if i % 2 == 0:
            name = "Operation"
            duration = 45
            t_tags = [ok.id]

            task = Task(
                name=name,
                duration=duration,
                time=datetime.now() - timedelta(days=i),
                tags=t_tags,
            )
            tasks_project_2.append(task)

tasks_project_3 = []
for i in range(100):
    if i not in [0, 6, 7]:
        if i % 5 == 0:
            name = "Analytics"
            duration = 240
            if i % 2 == 0:
                t_tags = [ok.id]
            else:
                t_tags = [firefighting.id]

            task = Task(
                name=name,
                duration=duration,
                time=datetime.now() - timedelta(days=i),
                tags=t_tags,
            )
            tasks_project_3.append(task)

list_tasks = [
    *tasks_civ,
    *tasks_elden_ring,
    *tasks_pull_ups,
    *tasks_push_ups,
    *tasks_sit_ups,
    *tasks_strech,
    *tasks_platform,
    *tasks_project_1,
    *tasks_project_2,
    *tasks_project_3,
]

# Topics
training = Topic(
    name="Training",
    tasks=[
        *[i.id for i in tasks_strech],
        *[i.id for i in tasks_sit_ups],
        *[i.id for i in tasks_pull_ups],
        *[i.id for i in tasks_push_ups],
    ],
)
gaming = Topic(
    name="Gaming",
    tasks=[
        *[i.id for i in tasks_elden_ring],
        *[i.id for i in tasks_civ],
    ],
)

platform = Topic(
    name="Platform",
    bookingNumber="DFE2",
    tasks=[i.id for i in tasks_platform],
)
project_1 = Topic(
    name="Project_1",
    bookingNumber="AFE",
    tasks=[i.id for i in tasks_project_1],
)
project_2 = Topic(
    name="Project_2",
    bookingNumber="DFE1",
    tasks=[i.id for i in tasks_project_2],
)
project_3 = Topic(
    name="Project_3",
    bookingNumber="VFE",
    tasks=[i.id for i in tasks_project_3],
)

list_topics = [training, gaming, platform, project_1, project_2, project_3]

# Areas
private = Area(name="Private", topics=[i.id for i in list_topics[:2]])
work = Area(name="Work", topics=[i.id for i in list_topics[2:]])

# containers
areas = {work.id: work, private.id: private}
topics = {t.id: t for t in list_topics}
tasks = {t.id: t for t in list_tasks}
tags = {t.id: t for t in list_tags}

PRESET_TEST = DataBaseSchema(
    areas=areas,
    topics=topics,
    tasks=tasks,
    tags=tags,
)
