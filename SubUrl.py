from enum import Enum

from api.SchoolLevel import SchoolLevel


class SubUrl(Enum):
    MEAL = "mealServiceDietInfo"
    INFO = "schoolInfo"
    TIME_TABLE = SchoolLevel
    SCHOOL_SCHEDULE = 'SchoolSchedule'

