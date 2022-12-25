from datetime import datetime
from typing import Sequence, Any

from discord import Embed, Colour
from .common.consts import KEY_NAMES

from .responses.MealServiceResponse import meal_names
from .SchoolApi import SchoolApi
from .RequestParameters import RequestParameters
from .StatusCodeError import StatusCodeError


class Embeds:
    @classmethod
    async def meal_service(cls, params: Sequence[RequestParameters], now_date: datetime, date: datetime,
                           school_name: str):
        formatted_date = date.strftime('%Y년 %m월 %d일')
        description = f"{school_name}의 {formatted_date}의 급식"
        embed = Embed(title="급식", colour=Colour.random(), description=description)

        for i, meal_name in enumerate(meal_names[3:]):
            try:
                meal_response = await SchoolApi.request_meal_service(params=params[i])
                cal_info = f"**총 칼로리**: {meal_response.CAL_INFO}"
                menu_info = "\n".join(meal_response.dish).replace("(", "").replace(")", "")
                nutrient_of_dish_info = "\n".join(
                    f"{k}: {v.replace('R.E', 'RE')} " for k, v in meal_response.nutrient_info.items())
                embed.add_field(name=meal_name, value=f"{cal_info}\n\n{menu_info}\n\n**영양정보**\n{nutrient_of_dish_info}")
            except StatusCodeError as e:
                if str(e) == StatusCodeError.errors["INFO-200"]:
                    embed.add_field(name=meal_name, value="없음")

        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2771/2771406.png")
        embed.timestamp = now_date

        return embed

    @classmethod
    async def time_table(cls, params: RequestParameters, data: dict[str, Any], now_date: datetime, date: datetime):
        formatted_date = date.strftime('%Y년 %m월 %d일')
        description = f"{data['school_name']} {data['grade']}학년 {data['class_name']}반의 {formatted_date}의 시간표"
        embed = Embed(title="시간표", colour=Colour.random(), description=description)

        try:
            time_table_response = await SchoolApi.request_time_table(params=params)
            time_table_info = "\n".join(time_table_response.time_table)
            embed.add_field(name="시간표", value=time_table_info)
        except StatusCodeError as e:
            if str(e) == StatusCodeError.errors["INFO-200"]:
                embed.add_field(name="시간표", value="없음")

        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/439/439296.png")
        embed.timestamp = now_date

        return embed

    @classmethod
    async def school_schedule(cls, params: RequestParameters, school_name: str, now_date: datetime, from_date: datetime,
                              to_date: datetime):
        formatted_term = f"{from_date.strftime('%Y')}~{to_date.strftime('%Y')}"
        embed = Embed(title="학사일정", colour=Colour.random(), description=f"{school_name}의 {formatted_term}의 학사일정")

        try:
            school_schedule_response = await SchoolApi.request_school_schedule(params=params)
            school_schedule_info = "\n".join(
                f"{day} : {name}" for name, day in school_schedule_response.schedule.items())
            embed.add_field(name="학사일정", value=school_schedule_info)
        except StatusCodeError as e:
            if str(e) == StatusCodeError.errors["INFO-200"]:
                embed.add_field(name="학사일정", value="조회 안됨")

        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2602/2602414.png")
        embed.timestamp = now_date

        return embed

    @classmethod
    async def school_schedule_notification(cls, params: RequestParameters, school_name: str, now_date: datetime):
        formatted_now_date = now_date.strftime("%Y/%m/%d")
        embed = Embed(title="학사일정", colour=Colour.random(), description=f"{school_name}의 오늘의 학사일정")
        try:
            school_schedule_response = await SchoolApi.request_school_schedule(params=params)
            school_schedule_info = school_schedule_response.schedule2[formatted_now_date]
            embed.add_field(name="학사일정", value=school_schedule_info)

        except StatusCodeError as e:
            if str(e) == StatusCodeError.errors["INFO-200"]:
                embed.add_field(name="학사일정", value="없음")

        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2602/2602414.png")
        embed.timestamp = now_date

        return embed

    @classmethod
    async def adding_notification(cls, user_name: str, data: dict[str, Any]):
        embed = Embed(title="설정한 알림들", colour=Colour.random(), description=f"{user_name}의 설정한 알림들")

        for key, value in KEY_NAMES.items():
            if value in data:
                embed.add_field(name=key, value=data[value])
            else:
                embed.add_field(name=key, value="미지정")

        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/545/545674.png")

        return embed
