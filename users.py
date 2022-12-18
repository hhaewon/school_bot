import asyncio
import datetime

from discord import SlashCommandGroup, ApplicationContext, Option, Embed, Colour

from libs.common.consts import KST, KEY_NAMES, KEY_NAMES_CHOICES
from libs.common.config import conf
from libs import RequestParameters, get_region_code, SchoolApi, StatusCodeError, region_choices, utils, COLLECTION, \
    Embeds

users = SlashCommandGroup(name="회원", description="정보 저장")
notification = users.create_subgroup(name="알림", description="알림 설정", guild_ids=conf().TEST_GUILD_ID)


@users.command(name="저장", description="정보를 저장합니다.", guild_ids=conf().TEST_GUILD_ID)
async def users_save_information(context: ApplicationContext,
                                 region: Option(str, description="저장할 지역명 (예: 강원, 경기, 서울, 충북)", name="지역명",
                                                choices=region_choices),
                                 school_name: Option(str, description="저장할 학교명 (예: 반곡중학교, 강남중학교)", name="학교명"),
                                 grade: Option(int, description="저장할 학년 (1, 2, 3, 4, 5, 6 중 하나)", name="학년",
                                               choices=[1, 2, 3, 4, 5, 6]),
                                 class_name: Option(int, description="저장할 반", name="반")):
    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(region),
        SCHUL_NM=school_name,
    )

    await context.response.defer()
    await asyncio.sleep(0.01)

    try:
        school_response = await SchoolApi.request_school_info(params=params)
    except StatusCodeError:
        await context.followup.send("잘못된 입력입니다.")
        return

    former_data = COLLECTION.find_one(filter={"id": context.user.id})
    data = {
        "id": context.user.id,
        "region": region,
        "school_name": school_name,
        "school_code": school_response.SD_SCHUL_CODE,
        "grade": grade,
        "class_name": class_name,
    }
    try:
        if former_data is None:
            COLLECTION.insert_one(document=data)
        else:
            new_values = {"$set": data}
            COLLECTION.update_one(filter={'id': context.user.id}, update=new_values)
        await context.followup.send("저장을 완료했습니다.")
    except Exception as e:
        print(e)
        await context.followup.send("저장 중 오류가 발생했습니다.")


@users.command(name="확인", description="저장된 회원 정보를 확인합니다.", guild_ids=conf().TEST_GUILD_ID)
async def user_check_information(context: ApplicationContext):
    data = COLLECTION.find_one(filter={"id": context.user.id})

    await context.response.defer()
    await asyncio.sleep(0.01)

    if data is None:
        await context.followup.send("저장된 회원이 아닙니다. 저장을 먼저 해주세요.")
        return

    embed = Embed(title="회원 정보", colour=Colour.random(), description=f"{context.user.mention}의 정보")
    embed.add_field(name="지역", value=data["region"])
    embed.add_field(name="학교명", value=data["school_name"])
    embed.add_field(name="학년", value=data["grade"])
    embed.add_field(name="반", value=data["class_name"])
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/545/545674.png")
    embed.timestamp = datetime.datetime.now()

    await context.followup.send(embed=embed)


@users.command(name="삭제", description="저장된 회원 정보를 삭제합니다.", guild_ids=conf().TEST_GUILD_ID)
async def user_delete_information(context: ApplicationContext):
    data = COLLECTION.find_one(filter={"id": context.user.id})

    await context.response.defer()
    await asyncio.sleep(0.01)

    if data is None:
        await context.followup.send("저장된 회원이 아닙니다. 저장을 먼저 해주세요.")
        return

    COLLECTION.delete_one(filter={"id": context.user.id})

    await context.followup.send("회원 정보 삭제를 완료했습니다.")


@users.command(name="시간표", description="저장된 정보로 시간표를 가져옵니다.", guild_ids=conf().TEST_GUILD_ID)
async def users_time_table(context: ApplicationContext,
                           day: Option(str, description="어제, 오늘, 내일, 모레 또는 연도-월-일 형식의 시간표를 가져올 날짜", name="날짜")):
    data = COLLECTION.find_one(filter={'id': context.user.id})

    await context.response.defer()
    await asyncio.sleep(0.01)

    if data is None:
        await context.followup.send("저장된 회원이 아닙니다. 저장을 먼저 해주세요.")
        return

    try:
        now_date, date = utils.get_date(day=day, timezone_=KST)
    except ValueError:
        await context.followup.send("잘못된 날짜 형식입니다. 연도-월-일 형식으로 입력해주세요.")
        return

    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(data["region"]),
        SCHUL_NM=data["school_name"],
        SD_SCHUL_CODE=data["school_code"],
        GRADE=str(data["grade"]),
        CLASS_NM=str(data["class_name"]),
        ALL_TI_YMD=date.strftime("%Y%m%d"),
    )

    embed = await Embeds.time_table(params=params, data=data, now_date=now_date, date=date)

    await context.followup.send(embed=embed)


@users.command(name="급식", description="저장된 정보로 급식 정보를 가져옵니다.", guild_ids=conf().TEST_GUILD_ID)
async def users_meal_service(context: ApplicationContext,
                             day: Option(str, description="어제, 오늘, 내일, 모레 또는 연도-월-일 형식의 시간표를 가져올 날짜", name="날짜")):
    data = COLLECTION.find_one(filter={'id': context.user.id})

    await context.response.defer()
    await asyncio.sleep(0.01)

    if data is None:
        await context.followup.send("저장된 회원이 아닙니다. 저장을 먼저 해주세요.")
        return

    try:
        now_date, date = utils.get_date(day=day, timezone_=KST)
    except ValueError:
        await context.followup.send("잘못된 날짜 형식입니다. 연도-월-일 형식으로 입력해주세요.")
        return

    params = tuple(RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(data["region"]),
        SCHUL_NM=data["school_name"],
        SD_SCHUL_CODE=data["school_code"],
        MLSV_YMD=date.strftime("%Y%m%d"),
        MMEAL_SC_CODE=str(i),
    ) for i in range(1, 4))

    embed = await Embeds.meal_service(params=params, now_date=now_date, date=date, school_name=data["school_name"])

    await context.followup.send(embed=embed)


@users.command(name="학사일정", description="저장된 정보로 급식 정보를 가져옵니다.", guild_ids=conf().TEST_GUILD_ID)
async def users_school_schedule(context: ApplicationContext,
                                school_year: Option(str,
                                                    description="작년, 올해, 내년 또는 연도 형식의 학사일정을 가져올 학년도 (예 2022, 2010)",
                                                    name="학년도")
                                ):
    data = COLLECTION.find_one(filter={'id': context.user.id})

    await context.response.defer()
    await asyncio.sleep(0.01)

    if data is None:
        await context.followup.send("저장된 회원이 아닙니다. 저장을 먼저 해주세요.")
        return

    try:
        now_date, from_date, to_date = utils.get_school_year_date(school_year=school_year, timezone_=KST)
    except ValueError:
        await context.followup.send("잘못된 학년도 형식입니다. 연도 형식으로 입력해주세요 (예 2022, 2010)")
        return

    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code(data["region"]),
        SCHUL_NM=data["school_name"],
        SD_SCHUL_CODE=data["school_code"],
        AA_FROM_YMD=from_date.strftime("%Y%m%d"),
        AA_TO_YMD=to_date.strftime("%Y%m%d"),
    )

    embed = await Embeds.school_schedule(params=params, school_name=data["school_name"], now_date=now_date,
                                         from_date=from_date, to_date=to_date)

    await context.followup.send(embed=embed)


@notification.command(name="추가", description="알림을 추가합니다. (이미 설정된 알림이면 변경합니다.)", guild_ids=conf().TEST_GUILD_ID)
async def add_notification(context: ApplicationContext,
                           name: Option(str, name="이름", description="급식, 시간표, 학사일정 중 하나인 알림을 받을 명령어의 이름 ",
                                        choices=KEY_NAMES_CHOICES),
                           time: Option(str, name="시각",
                                        description="시간:분 형식 형식의 알림을 받을 시각 (예 08:20, 19:10)")):
    data = COLLECTION.find_one(filter={"id": context.user.id})

    await context.response.defer()
    await asyncio.sleep(0.01)

    if data is None:
        await context.followup.send("저장된 회원이 아닙니다. 저장을 먼저 해주세요.")
        return

    try:
        entered_datetime = datetime.datetime.strptime(time, "%H:%M")
        time_argument = entered_datetime.strftime("%H:%M")
    except Exception as e:
        print(e)
        await context.followup.send("잘못된 시각 형식입니다. 시간:분 형식으로 입력해주세요.")
        return

    if name not in KEY_NAMES:
        await context.followup.send("급식, 시간표, 학사일정 중 하나를 입력해주세요.")
        return

    COLLECTION.update_one(filter={"id": context.user.id}, update={'$set': {KEY_NAMES[name]: time_argument}})

    await context.followup.send("알림 추가가 완료되었습니다.")


@notification.command(name="확인", description="설정된 알림을 확인합니다.", guild_ids=conf().TEST_GUILD_ID)
async def check_notifications(context: ApplicationContext):
    data = COLLECTION.find_one(filter={"id": context.user.id})

    await context.response.defer()
    await asyncio.sleep(0.01)

    if data is None:
        await context.followup.send("저장된 회원이 아닙니다. 저장을 먼저 해주세요.")
        return

    embed = await Embeds.adding_notification(user_name=context.user.name, data=data)

    await context.followup.send(embed=embed)


@notification.command(name="삭제", description="지정한 알림을 삭제합니다.", guild_ids=conf().TEST_GUILD_ID)
async def delete_notification(context: ApplicationContext,
                              notification_name: Option(str, name="이름", description="삭제할 알림 이름",
                                                        choices=KEY_NAMES_CHOICES)):
    data = COLLECTION.find_one(filter={"id": context.user.id})

    await context.response.defer()
    await asyncio.sleep(0.01)

    if data is None:
        await context.followup.send("저장된 회원이 아닙니다. 저장을 먼저 해주세요.")
        return

    if KEY_NAMES[notification_name] not in data:
        await context.followup.send("지정한 알림이 추가되지 않았습니다. 알림을 추가해야 삭제할 수 있습니다.")
        return

    COLLECTION.update_one(filter={"id": context.user.id}, update={"$unset": {KEY_NAMES[notification_name]: True}})

    await context.followup.send("삭제를 완료했습니다.")
