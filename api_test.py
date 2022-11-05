from lib.RequestParameters import RequestParameters
from lib.responses import MealServiceResponse, TimeTableResponse, MiddleTimeTableRow, SchoolScheduleResponse
from lib.SchoolApi import SchoolApi
from lib.region import get_region_code
import asyncio


async def main():
    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code("강원"),
        SCHUL_NM="반곡중학교",
        MLSV_YMD="20221011",
        MMEAL_SC_CODE="2",
        ALL_TI_YMD="20221104",
        GRADE="1",
        CLASS_NM="4",
        AA_FROM_YMD="202203",
        AA_TO_YMD="202303"
    )
    school_params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code("강원"),
        SCHUL_NM="반곡중학교",
    )
    school_info_response = await SchoolApi.request_school_info(params=school_params)
    params.SD_SCHUL_CODE = school_info_response.SD_SCHUL_CODE

    meal_service_response: MealServiceResponse
    time_table_response: TimeTableResponse[MiddleTimeTableRow]
    school_schedule_response: SchoolScheduleResponse
    meal_service_response, time_table_response, school_schedule_response = await asyncio.gather(
        SchoolApi.request_meal_service(params=params),
        SchoolApi.request_time_table(params=params),
        SchoolApi.request_school_schedule(params=params))
    print(meal_service_response)
    print(meal_service_response.ATPT_OFCDC_SC_CODE)
    print(meal_service_response.CAL_INFO)
    print(meal_service_response.nutrient_info)
    print(meal_service_response.country_of_origin_info)
    print(meal_service_response.DDISH_NM)

    print(time_table_response.time_table)
    print(time_table_response)
    print(time_table_response._rows)

    print(school_schedule_response)
    print(len(school_schedule_response.rows))
    print(school_schedule_response.schedule)
    print(school_schedule_response.schedule.items())
    print(school_schedule_response.schedule2)
    print(len(school_schedule_response.schedule2))
    print(len(school_schedule_response.schedule))

# {'3·1절': '2021/03/01',
# '입학식': '2021/03/02',
# '학부모총회': '2021/03/24',
# '학부모상담주간': '2021/10/15',
# '수업공개의 날': '2021/10/14',
# '1학년 영어듣기평가': '2021/09/07',
# '2학년 영어듣기평가': '2021/09/08',
# '3학년 영어듣기평가': '2021/09/09',
# '과학행사': '2021/04/16',
# '재량휴업일': '2021/11/18',
# '어린이날': '2021/05/05',
# '3학년 진로체험의 날': '2021/05/13',
# '부처님오신날(석가탄신일)': '2021/05/19',
# '체육대회': '2021/05/21',
# '2학년1회고사': '2021/11/26',
# '3학년1회고사': '2021/10/26',
# '방학식': '2021/07/20',
# '여름방학': '2021/07/21 ~ 2021/08/16',
# '개학식': '2021/08/17',
# '추석연휴': '2021/09/22',
# '추석': '2021/09/21',
# '개천절': '2021/10/03',
# '대체휴일': '2021/10/11',
# '한글날': '2021/10/09',
# '푸른솔축제': '2021/12/23',
# '진로의날 행사': '2021/12/24',
# '기독탄신일(성탄절)': '2021/12/25',
# '종업식': '2022/01/03',
# '졸업식': '2022/01/03',
# '겨울방학': '2022/01/04 ~ 2022/02/28'}

if __name__ == '__main__':
    asyncio.run(main())
