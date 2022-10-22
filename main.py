import asyncio
import datetime
import os

import discord
from discord import Option, ApplicationContext, Embed, Colour

from api import RequestParameters, SchoolApi, StatusCodeError, allergy_info, get_region_code, region_choices, meal_names

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TOKEN = os.environ['DISCORD_TOKEN']

bot = discord.Bot()
KST = datetime.timezone(datetime.timedelta(hours=9))


@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')


@bot.slash_command(name="급식", description="지정된 날짜의 급식 정보를 가져옵니다.", guild_ids=[802077280074465280])
async def meal_service(context: ApplicationContext,
                       region: Option(str, description="급식 정보를 가져올 지역명 (예: 강원, 경기, 서울, 충북)", name="지역명",
                                      choices=region_choices),
                       school_name: Option(str, description="급식 정보를 가져올 학교명 (예: 반곡중학교, 강남중학교)", name="학교명"),
                       day: Option(str, description="어제, 오늘, 내일, 모레 또는 연도-월-일 형식의 급식 정보를 가져올 날짜",
                                   name="날짜"),
                       meal_code: Option(str, description="아침, 점심, 저녁, 조식, 중식, 석식 중 하나", name="급식명",
                                         choices=meal_names, default="점심")):
    now_date = datetime.datetime.now(tz=KST)
    if day == "어제":
        date = now_date - datetime.timedelta(days=1)
    elif day == "오늘":
        date = now_date
    elif day == "내일":
        date = now_date + datetime.timedelta(days=1)
    elif day == "모레":
        date = now_date + datetime.timedelta(days=2)
    else:
        date = datetime.datetime.strptime(day, "%Y-%m-%d")

    if meal_code in ["아침", "조식"]:
        meal_code = "1"
    elif meal_code in ["점심", "중식"]:
        meal_code = "2"
    else:
        meal_code = "3"

    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(region),
        SCHUL_NM=school_name,
        MLSV_YMD=date.strftime("%Y%m%d"),
        MMEAL_SC_CODE=meal_code,
    )

    try:
        school_info_response = await SchoolApi.request_school_info(params=params)
        params.SD_SCHUL_CODE = school_info_response.SD_SCHUL_CODE
    except StatusCodeError as e:
        if str(e) == "해당하는 데이터가 없습니다.":
            await context.respond("잘못된 입력입니다.")
        return
    try:
        meal_response = await SchoolApi.request_meal_service(params=params)

        menu_info = "\n".join(meal_response.dish)
        country_of_origin_info = "\n".join([f"{k} : {v}" for k, v in meal_response.country_of_origin_info.items()])
        nutrient_info = "\n".join([f"{k} : {v}".replace("R.E", "RE") for k, v in meal_response.nutrient_info.items()])
        calorie_info = meal_response.CAL_INFO
        allergy_info_ = "\n".join([f"{k} : {v}" for k, v in allergy_info.items()])

        embed = Embed(title="급식", colour=Colour.random(), description=f"{meal_response.MLSV_YMD}의 급식")
        embed.add_field(name="메뉴", value=menu_info)
        embed.add_field(name="영양정보", value=nutrient_info)
        embed.add_field(name="칼로리", value=calorie_info)
        embed.add_field(name="원산지", value=country_of_origin_info)
        embed.add_field(name="알레르기 정보", value=allergy_info_)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2771/2771406.png")
        embed.timestamp = now_date

        await context.respond(embed=embed)
    except StatusCodeError as e:
        if str(e) == "해당하는 데이터가 없습니다.":
            await context.respond("이 날은 급식이 없습니다.")


@bot.slash_command(name="시간표", description='지정된 날짜의 시간표를 가져옵니다.')
async def time_table(context: ApplicationContext,
                     region: Option(str, description="시간표를 가져올 지역명 (예: 강원, 경기, 서울, 충북)", name="지역명",
                                    choices=region_choices),
                     school_name: Option(str, description="시간표를 가져올 학교명 (예: 반곡중학교, 강남중학교)", name="학교명"),
                     grade: Option(int, description="시간표를 가져올 학년 (1, 2, 3, 4, 5, 6 중 하나)", name="학년",
                                   choices=[1, 2, 3, 4, 5, 6]),
                     class_name: Option(int, description="시간표를 가져올 반", name="반"),
                     day: Option(str, description="어제, 오늘, 내일, 모래 또는 연도-월-일 형식의 시간표를 가져올 날짜", name="날짜")):
    now_date = datetime.datetime.now(tz=KST)
    if day == "어제":
        date = now_date - datetime.timedelta(days=1)
    elif day == "오늘":
        date = now_date
    elif day == "내일":
        date = now_date + datetime.timedelta(days=1)
    elif day == "모레":
        date = now_date + datetime.timedelta(days=2)
    else:
        date = datetime.datetime.strptime(day, "%Y-%m-%d")

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
        await context.respond("잘못된 입력입니다.")
        return

    try:
        if school_name.endswith('초등학교'):
            meal_response = await SchoolApi.request_elementary_time_table(params=params)
        elif school_name.endswith('중학교'):
            meal_response = await SchoolApi.request_middle_time_table(params=params)
        elif school_name.endswith('고등학교'):
            meal_response = await SchoolApi.request_high_time_table(params=params)
        else:
            await context.send("잘못된 학교 이름입니다.")
            return

        time_table_info = "\n".join(meal_response.time_table)
        embed = Embed(title="시간표", colour=Colour.random(), description=f"{meal_response.rows[0].ALL_TI_YMD}의 시간표")
        embed.add_field(name="시간표", value=time_table_info)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/439/439296.png")
        embed.timestamp = now_date

        await context.respond(embed=embed)
    except StatusCodeError:
        await context.respond("입력값이 잘못되었습니다.")


@bot.slash_command(name="학사일정", description='지정된 학년도의 학사일정을 가져옵니다.')
async def school_schedule(context: ApplicationContext,
                          region: Option(str, description="학사일정을 가져올 지역 (예: 강원, 경기, 서울, 충북)", name="지역명",
                                         choices=region_choices),
                          school_name: Option(str, "학사일정을 가져올 학교명  (예: 반곡중학교, 강남중학교)", name="학교명"),
                          school_year: Option(str, description="작년, 올해, 내년 또는 연도 형식의 학사일정을 가져올 학년도 (예 2022, 2010)",
                                              name="학년도")):
    now_date = datetime.datetime.now(tz=KST)

    if school_year == "작년":
        from_date = now_date.replace(year=now_date.year - 1, month=3)
        to_date = now_date.replace(year=now_date.year, month=3)
    elif school_year == '올해':
        from_date = now_date.replace(year=now_date.year, month=3)
        to_date = now_date.replace(year=now_date.year + 1, month=3)
    elif school_year == '내년':
        from_date = now_date.replace(year=now_date.year + 1, month=3)
        to_date = now_date.replace(year=now_date.year + 2, month=3)
    else:
        date = datetime.datetime.strptime(str(school_year), "%Y")
        from_date = date.replace(month=3)
        to_date = date.replace(year=date.year + 1, month=3)

    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(region),
        SCHUL_NM=school_name,
        AA_FROM_YMD=from_date.strftime("%Y%m"),
        AA_TO_YMD=to_date.strftime("%Y%m")
    )

    try:
        school_response = await SchoolApi.request_school_info(params=params)
        params.SD_SCHUL_CODE = school_response.SD_SCHUL_CODE
    except StatusCodeError:
        await context.respond("잘못된 입력입니다.")
        return

    try:
        schedule_response = await SchoolApi.request_school_schedule(params=params)

        embed = Embed(title="시간표", colour=Colour.random(),
                      description=f"{from_date.strftime()}~{to_date.strftime()}의 학사일정")
        school_schedule_info = "\n".join(f"{day} : {name}" for name, day in schedule_response.schedule.items())
        embed.add_field("학사일정", value=school_schedule_info)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2602/2602414.png")
        embed.timestamp = now_date

        await context.respond(embed=embed)
    except StatusCodeError:
        print('잘못된 입력입니다.')


bot.run(TOKEN)
