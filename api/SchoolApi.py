import json
from dataclasses import asdict

import requests

from api.SubUrl import SubUrl
from api.responses.MealServiceResponse import MealServiceResponse
from api.responses.SchoolInfoResponse import SchoolInfoResponse
from api.responses.TimeTableResponse import ElementaryTimeTableResponse, MiddleTimeTableResponse, HighTimeTableResponse
from api.RequestParameters import RequestParameters
from api.StatusCodeError import StatusCodeError


class SchoolApi:
    BASE_URL = "https://open.neis.go.kr/hub/"

    @classmethod
    def request_meal_service(cls, params: RequestParameters) -> MealServiceResponse:
        row = cls._get_requests(url=cls.BASE_URL + SubUrl.MEAL,
                                service_name=SubUrl.MEAL,
                                params=params)
        return MealServiceResponse(**row)

    @classmethod
    def request_school_info(cls, params: RequestParameters) -> SchoolInfoResponse:
        row = cls._get_requests(url=cls.BASE_URL + SubUrl.INFO,
                                service_name=SubUrl.INFO,
                                params=params)
        return SchoolInfoResponse(**row)

    @classmethod
    def request_elementary_time_table(cls, params: RequestParameters) -> ElementaryTimeTableResponse:
        row = cls._get_requests(url=cls.BASE_URL + SubUrl.ELEMENTARY_TIME_TABLE,
                                service_name=SubUrl.ELEMENTARY_TIME_TABLE,
                                params=params)
        return ElementaryTimeTableResponse(**row)

    @classmethod
    def request_middle_time_table(cls, params: RequestParameters) -> MiddleTimeTableResponse:
        row = cls._get_requests(url=cls.BASE_URL + SubUrl.MIDDLE_TIME_TABLE,
                                service_name=SubUrl.MIDDLE_TIME_TABLE,
                                params=params)
        return MiddleTimeTableResponse(**row)

    @classmethod
    def request_high_time_table(cls, params: RequestParameters) -> HighTimeTableResponse:
        row = cls._get_requests(url=cls.BASE_URL + SubUrl.HIGH_TIME_TABLE,
                                service_name=SubUrl.HIGH_TIME_TABLE,
                                params=params)
        return HighTimeTableResponse(**row)

    @classmethod
    def _get_requests(cls, url: str, service_name: str, params: RequestParameters) -> dict:
        response = requests.get(url=url, params=asdict(params))
        response.encoding = "UTF-8"

        text = response.text.replace("<br/>", "\n")
        json_response = cls._loads_json(json_string=text)
        status_code = cls._get_status_code(json_response=json_response, key=service_name)
        cls._check_status_code(status_code=status_code)

        return cls._get_row_data(json_response=json_response, service_name=service_name)

    @classmethod
    def _loads_json(cls, json_string: str) -> dict:
        return json.loads(s=json_string, strict=False)

    @classmethod
    def _get_status_code(cls, json_response: dict, key: str) -> str:
        try:
            status_code = json_response[key][0]["head"][1]["RESULT"]["CODE"]
        except KeyError:
            status_code = json_response["RESULT"]["CODE"]
        return status_code

    @classmethod
    def _check_status_code(cls, status_code: str) -> None:
        if status_code.startswith("INFO"):
            return
        elif status_code.startswith("ERROR"):
            raise StatusCodeError(error_code=status_code)

    @classmethod
    def _get_row_data(cls, json_response: dict, service_name: str) -> dict:
        return json_response[service_name][1]["row"][0]


