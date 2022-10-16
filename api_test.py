from api.request.RequestParameters import RequestParameters
from api.request.SchoolApi import SchoolApi
from api.request.region import get_region_code


params = RequestParameters(
    ATPT_OFCDC_SC_CODE=get_region_code("강원"),
    SCHUL_NM="반곡중학교",
    MLSV_YMD="20221011",
    MMEAL_SC_CODE="2",
    ALL_TI_YMD="20221011",
    GRADE="1",
    CLASS_NM="4",
    AA_FROM_YMD="202103",
    AA_TO_YMD="202203"
)

school_info_response = SchoolApi.request_school_info(params=params)
print(school_info_response)

school_info_response = SchoolApi.request_school_info(params=params)
params.SD_SCHUL_CODE = school_info_response.SD_SCHUL_CODE

meal_service_response = SchoolApi.request_meal_service(params=params)
print(meal_service_response)
print(meal_service_response.ATPT_OFCDC_SC_CODE)
print(meal_service_response.nutrient_info)
print(meal_service_response.country_of_origin_info)
print(meal_service_response.dish)

time_table_response = SchoolApi.request_middle_time_table(params=params)
print(time_table_response.time_table)
print(time_table_response)
print(time_table_response._rows)

school_schedule_response = SchoolApi.request_school_schedule(params=params)
print(school_schedule_response)
print(school_schedule_response.schedule)
# print(len(response.schedule))