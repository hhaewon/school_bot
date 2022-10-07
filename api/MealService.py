from dataclasses import dataclass


@dataclass(kw_only=True)
class MealResult:
    ATPT_OFCDC_SC_CODE: str
    ATPT_OFCDC_SC_NM: str
    SD_SCHUL_CODE: str
    SCHUL_NM: str
    MMEAL_SC_CODE: str
    MMEAL_SC_NM: str
    MLSV_YMD: str
    MLSV_FGR: str
    DDISH_NM: str
    ORPLC_INFO: str
    CAL_INFO: str
    NTR_INFO: str
    MLSV_FROM_YMD: str
    MLSV_TO_YMD: str


class MealService:
    def __init__(self, meal_result: MealResult):
        self.meal_result = meal_result

    @property
    def dish(self):
        dish_list = self.meal_result.DDISH_NM.split("\n")
        for dish in dish_list:
            yield dish

    @property
    def country_of_origin_info(self):
        country_of_origin_list = self.meal_result.ORPLC_INFO.split("\n")
        for country_of_origin in country_of_origin_list:
            yield country_of_origin

    @property
    def nutrient_info(self):
        nutrient_info_list = self.meal_result.NTR_INFO.split("\n")
        nutrient_info_dict = dict()
        for nutrient_info in nutrient_info_list:
            parentheses_start_index = nutrient_info.index("(")
            parentheses_end_index = nutrient_info.index(")")
            unit = nutrient_info[parentheses_start_index + 1:parentheses_end_index]
            nutrient = nutrient_info[:parentheses_start_index]
            degree = nutrient_info.split(": ")[-1]
            nutrient_info_dict[nutrient] = f"{degree}{unit}"

        return nutrient_info_dict