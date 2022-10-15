import asyncio
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Context

from api.request.RequestParameters import RequestParameters
from api.request.SchoolApi import SchoolApi
from api.request.StatusCodeError import StatusCodeError
from api.request.region import get_region_code
from utils import get_token

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TOKEN = get_token("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')


@bot.command()
async def 급식(context: Context,
             region: str, school_name: str, day: str, meal_code: str = '2'):
    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(region),
        SCHUL_NM=school_name,
        MLSV_YMD=day,
        MMEAL_SC_CODE=meal_code,
    )

    try:
        response = SchoolApi.request_school_info(params=params)
        params.SD_SCHUL_CODE = response.SD_SCHUL_CODE

        response = SchoolApi.request_meal_service(params=params)
        await context.send('\n'.join(response.dish))
    except StatusCodeError:
        await context.send('잘못된 입력입니다.')


@bot.command()
async def 시간표(context: Context, region: str, school_name: str, grade: str, class_name: str, day: str):
    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(region),
        SCHUL_NM=school_name,
        GRADE=grade,
        CLASS_NM=class_name,
        ALL_TI_YMD=day,
    )

    school_response = None
    meal_response = None

    try:
        school_response = SchoolApi.request_school_info(params=params)
        params.SD_SCHUL_CODE = school_response.SD_SCHUL_CODE
    except StatusCodeError:
        await context.send("잘못된 입력입니다.")
        return

    try:
        if school_name.endswith('초등학교'):
            meal_response = SchoolApi.request_elementary_time_table(params=params)
        elif school_name.endswith('중학교'):
            meal_response = SchoolApi.request_middle_time_table(params=params)
        elif school_name.endswith('고등학교'):
            meal_response = SchoolApi.request_high_time_table(params=params)
        else:
            await context.send("잘못된 학교 이름입니다.")
            return
        await context.send('\n'.join(meal_response.time_table))
    except StatusCodeError:
        await context.send("입력값이 잘못되었습니다.")


@bot.command()
async def 학사일정(context: Context, region: str, school_name: str, school_year: str):
    result_string = ""

    date = datetime.datetime.strptime(school_year, "%Y")
    from_date = date.replace(month=3)
    to_date = date.replace(year=date.year + 1, month=3)

    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(region),
        SCHUL_NM=school_name,
        AA_FROM_YMD=from_date.strftime("%Y%m"),
        AA_TO_YMD=to_date.strftime("%Y%m")
    )

    try:
        school_response = SchoolApi.request_school_info(params=params)
        params.SD_SCHUL_CODE = school_response.SD_SCHUL_CODE

        schedule_response = SchoolApi.request_school_schedule(params=params)
        for name, day in schedule_response.schedule.items():
            result_string += f'{day}: {name}\n'

        await context.send(result_string)
    except StatusCodeError:
        print('잘못된 입력입니다.')


bot.run(TOKEN)
