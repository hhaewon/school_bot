from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value


class SubUrl(StrEnum):
    MEAL = "mealServiceDietInfo"
    INFO = "schoolInfo"
    SCHOOL_SCHEDULE = "SchoolSchedule"
    ELEMENTARY = "elsTimetable"
    MIDDLE = "misTimetable"
    HIGH = "hisTimetable"
