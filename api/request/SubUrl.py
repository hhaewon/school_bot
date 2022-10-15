from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value


class SubUrl(StrEnum):
    MEAL: str = "mealServiceDietInfo"
    INFO: str = "schoolInfo"
    SCHOOL_SCHEDULE: str = "SchoolSchedule"
    ELEMENTARY_TIME_TABLE: str = "elsTimetable"
    MIDDLE_TIME_TABLE: str = "misTimetable"
    HIGH_TIME_TABLE: str = "hisTimetable"


