from libs.RequestParameters import RequestParameters
from libs.responses import MealServiceResponse, SchoolScheduleResponse, MiddleTimeTableRow
from libs.SchoolApi import SchoolApi
from libs.region import get_region_code
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
        AA_FROM_YMD="202103",
        AA_TO_YMD="202203"
    )
    school_params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code("강원"),
        SCHUL_NM="반곡중학교",
    )
    school_info_response = await SchoolApi.request_school_info(params=school_params)
    params.SD_SCHUL_CODE = school_info_response.SD_SCHUL_CODE

    meal_service_response: MealServiceResponse
    school_schedule_response: SchoolScheduleResponse
    time_table_response: MiddleTimeTableRow

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

    print(school_schedule_response)
    print(school_schedule_response.rows)
    print(school_schedule_response.schedule)
    print(school_schedule_response.schedule.items())
    print(school_schedule_response.schedule2)
    print(len(school_schedule_response.schedule2))
    print(len(school_schedule_response.schedule))


if __name__ == '__main__':
    asyncio.run(main())
