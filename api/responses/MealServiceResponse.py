from dataclasses import dataclass

meal_names = ["아침", "점심", "저녁", "조식", "중식", "석식"]

@dataclass(kw_only=True, slots=True)
class MealServiceResponse:
    """
    ATPT_OFCDC_SC_CODE: 시도교육청코드\n
    ATPT_OFCDC_SC_NM: 시도교육청명\n
    SD_SCHUL_CODE: 표준학교코드\n
    SCHUL_NM: 학교명\n
    MMEAL_SC_CODE: 식사코드\n
    MMEAL_SC_NM: 식사명\n
    MLSV_YMD: 급식일자\n
    MLSV_FGR: 급식인원수\n
    DDISH_NM: 요리명\n
    ORPLC_INFO: 원산지정보\n
    CAL_INFO: 칼로리정보\n
    NTR_INFO: 영양정보\n
    MLSV_FROM_YMD: 급식시작일자\n
    MLSV_TO_YMD: 급식종료일자\n
    dish: 요리명 리스트\n
    country_of_origin_info: 원산지 정보 딕셔너리\n
    nutrient_info: 영양 정보 딕셔너리\n
    """
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

    @property
    def dish(self) -> list[str]:
        return self.DDISH_NM.split("\n")

    @property
    def country_of_origin_info(self):
        country_of_origin_list = self.ORPLC_INFO.split("\n")
        country_of_origin_dict = dict()
        for country_of_origin in country_of_origin_list:
            key, value = country_of_origin.split(" : ")
            country_of_origin_dict[key] = value
        return country_of_origin_dict

    @property
    def nutrient_info(self):
        nutrient_info_list = self.NTR_INFO.split("\n")
        nutrient_info_dict = dict()
        for nutrient_info in nutrient_info_list:
            parentheses_start_index = nutrient_info.index("(")
            parentheses_end_index = nutrient_info.index(")")
            unit = nutrient_info[parentheses_start_index + 1:parentheses_end_index]
            nutrient = nutrient_info[:parentheses_start_index]
            degree = nutrient_info.split(": ")[-1]
            nutrient_info_dict[nutrient] = f"{degree}{unit}"

        return nutrient_info_dict

