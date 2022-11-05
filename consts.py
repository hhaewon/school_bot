import datetime
import os

import pymongo

TOKEN = os.environ['DISCORD_TOKEN']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']

TEST_GUILD_ID = 802077280074465280

KST = datetime.timezone(datetime.timedelta(hours=9))

URI = f"mongodb+srv://hhaewon:{MONGO_PASSWORD}@cluster0.gbbippl.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(URI)
collection = client['users']['users']

KEY_NAMES = {"급식": "meal_service_time",
             "시간표": "time_table_time",
             "학사일정": "school_schedule_time"}
KEY_NAMES_CHOICES = list(KEY_NAMES.keys())
KEY_NAMES_VALUES = KEY_NAMES.values()