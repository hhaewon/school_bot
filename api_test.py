import unittest
from dataclasses import asdict

from api.MealService import MealService, MealResult
from api.RequestParameters import RequestParameters
from api.SchoolApi import SchoolApi
from api.region import get_region_code


class TestApi(unittest.TestCase):
    params = RequestParameters(
        ATPT_OFCDC_SC_CODE=get_region_code("강원도교육청"),
        SCHUL_NM="반곡중학교",
        MLSV_YMD="20221007"
    )

    def test_load_school_info(self):
        response = SchoolApi.load_school_info(params=self.params)
        self.assertTrue(response)

    def test_load_meal_service(self):
        response = SchoolApi.load_school_info(params=self.params)
        self.params.SD_SCHUL_CODE = response["SD_SCHUL_CODE"]
        response = SchoolApi.load_meal_service(params=self.params)
        meal_result = MealResult(**response)
        meal_object = MealService(meal_result=meal_result)
        print(meal_object.nutrient_info)
        for item in meal_object.dish:
            print(item)
        for item in meal_object.country_of_origin_info:
            print(item)


