from api.RequestParameters import RequestParameters
from api.SchoolApi import SchoolApi
from api.region import get_region_code


params = RequestParameters(
    ATPT_OFCDC_SC_CODE=get_region_code("강원"),
    SCHUL_NM="반곡중학교",
    MLSV_YMD="20221011",
    MMEAL_SC_CODE="2",
    ALL_TI_YMD="20221011",
    GRADE="1",
    CLASS_NM="4",
)

response = SchoolApi.request_school_info(params=params)
print(response)

response = SchoolApi.request_school_info(params=params)
params.SD_SCHUL_CODE = response.SD_SCHUL_CODE
response = SchoolApi.request_meal_service(params=params)
print(response)
print(response.ATPT_OFCDC_SC_CODE)
print(response.nutrient_info)
print(response.country_of_origin_info)
print(response.dish)

response = SchoolApi.request_middle_time_table(params=params)
print(response)

