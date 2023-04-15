from libs import utils
from libs.api.RequestParameters import RequestParameters
from libs.api.responses import MealServiceResponse, SchoolScheduleResponse, MiddleTimeTableRow
from libs.api.SchoolApi import SchoolApi
from libs.common.consts import KEY_NAMES_VALUES, KST
from libs.database import Schema, COLLECTION
from libs.notification import send_meal_service_data, send_time_table_data, send_school_schedule_data
from libs.region import get_region_code
import asyncio

from pymongo.cursor import Cursor


async def main():
    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code("강원"),
        SCHUL_NM="반곡중학교",
        MLSV_YMD="20230324",
        MMEAL_SC_CODE="2",
        ALL_TI_YMD="20230324",
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

    meal_service_response: MealServiceResponse = await SchoolApi.request_meal_service(params=params)
    school_schedule_response: SchoolScheduleResponse = await SchoolApi.request_time_table(params=params)
    time_table_response: MiddleTimeTableRow = await SchoolApi.request_school_schedule(params=params)

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
    asyncio.get_event_loop().run_until_complete(main())
