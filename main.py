import asyncio

from discord import Option, ApplicationContext, Bot
from discord.ext import tasks
from pymongo.cursor import Cursor

from libs.RequestParameters import RequestParameters
from libs.SchoolApi import SchoolApi
from libs.StatusCodeError import StatusCodeError
from libs.region import get_region_code, region_choices
from libs import utils
from libs.database import COLLECTION, CLIENT, Schema
from libs.Embeds import Embeds

from libs.common.consts import TOKEN, KST, KEY_NAMES_VALUES
from libs.common.config import conf

from users import users

bot = Bot()


@bot.event
async def on_ready():
    send_notification.start()
    print(f'Login bot: {bot.user}')


@bot.slash_command(name="급식", description="지정된 날짜의 급식 정보를 가져옵니다.", guild_ids=conf().TEST_GUILD_ID)
async def meal_service(context: ApplicationContext,
                       region: Option(str, description="급식 정보를 가져올 지역명 (예: 강원, 경기, 서울, 충북)", name="지역명",
                                      choices=region_choices),
                       school_name: Option(str, description="급식 정보를 가져올 학교명 (예: 반곡중학교, 강남중학교)", name="학교명"),
                       day: Option(str, description="어제, 오늘, 내일, 모레 또는 연도-월-일 형식의 급식 정보를 가져올 날짜",
                                   name="날짜")):
    await context.response.defer()
    await asyncio.sleep(0)

    try:
        now_date, date = utils.get_date(day=day, timezone_=KST)
    except ValueError:
        await context.followup.send("잘못된 날짜 형식입니다. 연도-월-일 형식으로 입력해주세요.")
        return

    params = tuple(RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(region),
        SCHUL_NM=school_name,
        MLSV_YMD=date.strftime("%Y%m%d"),
        MMEAL_SC_CODE=str(i),
    ) for i in range(1, 4))

    embed = await Embeds.meal_service(params=params, now_date=now_date, date=date, school_name=school_name)
    await context.followup.send(embed=embed)


@bot.slash_command(name="시간표", description='지정된 날짜의 시간표를 가져옵니다.', guild_ids=conf().TEST_GUILD_ID)
async def time_table(context: ApplicationContext,
                     region: Option(str, description="시간표를 가져올 지역명 (예: 강원, 경기, 서울, 충북)", name="지역명",
                                    choices=region_choices),
                     school_name: Option(str, description="시간표를 가져올 학교명 (예: 반곡중학교, 강남중학교)", name="학교명"),
                     grade: Option(int, description="시간표를 가져올 학년 (1, 2, 3, 4, 5, 6 중 하나)", name="학년",
                                   choices=[1, 2, 3, 4, 5, 6]),
                     class_name: Option(int, description="시간표를 가져올 반", name="반"),
                     day: Option(str, description="어제, 오늘, 내일, 모레 또는 연도-월-일 형식의 시간표를 가져올 날짜", name="날짜")):
    await context.response.defer()
    await asyncio.sleep(0)

    try:
        now_date, date = utils.get_date(day=day, timezone_=KST)
    except ValueError:
        await context.followup.send("잘못된 날짜 형식입니다. 연도-월-일 형식으로 입력해주세요.")
        return

    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(region),
        SCHUL_NM=school_name,
        GRADE=str(grade),
        CLASS_NM=str(class_name),
        ALL_TI_YMD=date.strftime("%Y%m%d"),
    )

    try:
        school_response = await SchoolApi.request_school_info(params=params)
        params.SD_SCHUL_CODE = school_response.SD_SCHUL_CODE
    except StatusCodeError:
        await context.followup.send("잘못된 입력입니다.")
        return

    data = {
        "school_name": school_name,
        "grade": grade,
        "class_name": class_name
    }

    embed = await Embeds.time_table(params=params, data=data, now_date=now_date, date=date)

    await context.followup.send(embed=embed)


@bot.slash_command(name="학사일정", description='지정된 학년도의 학사일정을 가져옵니다.', guild_ids=conf().TEST_GUILD_ID)
async def school_schedule(context: ApplicationContext,
                          region: Option(str, description="학사일정을 가져올 지역 (예: 강원, 경기, 서울, 충북)", name="지역명",
                                         choices=region_choices),
                          school_name: Option(str, "학사일정을 가져올 학교명  (예: 반곡중학교, 강남중학교)", name="학교명"),
                          school_year: Option(str, description="작년, 올해, 내년 또는 연도 형식의 학사일정을 가져올 학년도 (예 2022, 2010)",
                                              name="학년도")):
    await context.response.defer()
    await asyncio.sleep(0)

    try:
        now_date, from_date, to_date = utils.get_school_year_date(school_year=school_year, timezone_=KST)
    except ValueError:
        await context.followup.send("잘못된 연도 형식입니다. 연도 형식으로 입력해주세요 (예 2022, 2010)")
        return

    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(region),
        SCHUL_NM=school_name,
        AA_FROM_YMD=from_date.strftime("%Y%m%d"),
        AA_TO_YMD=to_date.strftime("%Y%m%d")
    )

    try:
        school_response = await SchoolApi.request_school_info(params=params)
        params.SD_SCHUL_CODE = school_response.SD_SCHUL_CODE
    except StatusCodeError as e:
        if str(e) == "해당하는 데이터가 없습니다.":
            await context.followup.send("잘못된 입력입니다.")
            return
        else:
            await context.followup.send("오류가 발생했습니다.")
            return

    embed = await Embeds.school_schedule(params=params, school_name=school_name, now_date=now_date, from_date=from_date,
                                         to_date=to_date)

    await context.followup.send(embed=embed)


@tasks.loop(minutes=1.0)
async def send_notification():
    now_date, _ = utils.get_date(day="오늘", timezone_=KST)

    if 6 <= now_date.isoweekday():
        return

    now_time = now_date.strftime("%H:%M")
    now_full_date = now_date.strftime("%Y%m%d")
    meal_service_datas: Cursor[Schema]
    time_table_datas: Cursor[Schema]
    school_schedule_datas: Cursor[Schema]
    meal_service_datas, time_table_datas, school_schedule_datas = [COLLECTION.find(filter={key_name: now_time}) for
                                                                   key_name in KEY_NAMES_VALUES]
    for data in meal_service_datas:
        user = await bot.fetch_user(data['id'])
        params = tuple(RequestParameters(
            ATPT_OFCDC_SC_CODE=get_region_code(data["region"]),
            SCHUL_NM=data["school_name"],
            SD_SCHUL_CODE=data["school_code"],
            MLSV_YMD=now_full_date,
            MMEAL_SC_CODE=str(i),
        ) for i in range(1, 4))

        embed = await Embeds.meal_service(params=params, now_date=now_date, date=now_date,
                                          school_name=data["school_name"])
        await user.send(embed=embed)

    for data in time_table_datas:
        user = await bot.fetch_user(data['id'])
        params = RequestParameters(
            ATPT_OFCDC_SC_CODE=get_region_code(data["region"]),
            SCHUL_NM=data["school_name"],
            SD_SCHUL_CODE=data["school_code"],
            GRADE=str(data["grade"]),
            CLASS_NM=str(data["class_name"]),
            ALL_TI_YMD=now_full_date,
        )
        embed = await Embeds.time_table(params=params, data=data, date=now_date, now_date=now_date)
        await user.send(embed=embed)

    _, from_date, to_date = utils.get_school_year_date(school_year="올해", timezone_=KST)
    for data in school_schedule_datas:
        user = await bot.fetch_user(data['id'])

        params = RequestParameters(
            ATPT_OFCDC_SC_CODE=get_region_code(data["region"]),
            SCHUL_NM=data["school_name"],
            SD_SCHUL_CODE=data["school_code"],
            AA_FROM_YMD=from_date.strftime("%Y%m%d"),
            AA_TO_YMD=to_date.strftime("%Y%m%d"),
        )

        embed = await Embeds.school_schedule(params=params, school_name=data["school_name"], now_date=now_date,
                                             from_date=from_date, to_date=to_date)
        await user.send(embed=embed)


bot.add_application_command(users)
bot.run(TOKEN)
CLIENT.close()
