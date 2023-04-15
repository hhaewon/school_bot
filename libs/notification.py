from datetime import datetime

import discord
from discord import Bot
from libs.Embeds import Embeds
from libs.api.RequestParameters import RequestParameters
from libs.database import Schema
from libs.region import get_region_code


async def send_meal_service_data(bot: Bot, data: Schema, now_date: datetime):
    user = await bot.fetch_user(data['id'])
    params = tuple(RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(data["region"]),
        SCHUL_NM=data["school_name"],
        SD_SCHUL_CODE=data["school_code"],
        MLSV_YMD=now_date.strftime("%Y%m%d"),
        MMEAL_SC_CODE=str(i),
    ) for i in range(1, 4))

    embed = await Embeds.meal_service(params=params, now_date=now_date, date=now_date, school_name=data["school_name"])
    try:
        await user.send(embed=embed)
    except discord.Forbidden:
        pass


async def send_time_table_data(bot: Bot, data: Schema, now_date: datetime):
    user = await bot.fetch_user(data['id'])
    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(data["region"]),
        SCHUL_NM=data["school_name"],
        SD_SCHUL_CODE=data["school_code"],
        GRADE=str(data["grade"]),
        CLASS_NM=str(data["class_name"]),
        ALL_TI_YMD=now_date.strftime("%Y%m%d"),
    )
    embed = await Embeds.time_table(params=params, data=data, date=now_date, now_date=now_date)
    try:
        await user.send(embed=embed)
    except discord.Forbidden:
        pass


async def send_school_schedule_data(bot: Bot, data: Schema, from_date: datetime, to_date: datetime, now_date: datetime):
    user = await bot.fetch_user(data['id'])

    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(data["region"]),
        SCHUL_NM=data["school_name"],
        SD_SCHUL_CODE=data["school_code"],
        AA_FROM_YMD=from_date.strftime("%Y%m%d"),
        AA_TO_YMD=to_date.strftime("%Y%m%d"),
    )

    embed = await Embeds.school_schedule_notification(params=params, school_name=data["school_name"], now_date=now_date)
    try:
        await user.send(embed=embed)
    except discord.Forbidden:
        pass
