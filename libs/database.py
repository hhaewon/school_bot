import os
from typing_extensions import NotRequired
from typing import TypedDict

from pymongo import MongoClient


class Schema(TypedDict):
    id: int
    region: str
    school_name: str
    school_code: str
    grade: int
    class_name: int
    meal_service_time: NotRequired[str]
    time_table_time: NotRequired[str]
    school_schedule_time: NotRequired[str]


_MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
_URI = f"mongodb+srv://hhaewon:{_MONGO_PASSWORD}@cluster0.gbbippl.mongodb.net/?retryWrites=true&w=majority"
CLIENT: MongoClient[Schema] = MongoClient(_URI)
COLLECTION = CLIENT["users"]["users"]
