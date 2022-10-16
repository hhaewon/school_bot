import json
from dataclasses import asdict

import requests

from api.request.SubUrl import SubUrl
from api.request.responses.MealServiceResponse import MealServiceResponse
from api.request.responses.SchoolInfoResponse import SchoolInfoResponse
from api.request.responses.SchoolScheduleResponse import SchoolScheduleResponse, SchoolScheduleRow
from api.request.responses.TimeTableResponse import ElementaryTimeTableRow, MiddleTimeTableRow, HighTimeTableRow, \
    TimeTableResponse
from api.request.RequestParameters import RequestParameters
from api.request.StatusCodeError import StatusCodeError


class SchoolApi:
    BASE_URL = "https://open.neis.go.kr/hub/"

    @classmethod
    def request_meal_service(cls, params: RequestParameters) -> MealServiceResponse:
        row = cls._get_requests(url=cls.BASE_URL + SubUrl.MEAL,
                                service_name=SubUrl.MEAL,
                                params=params)
        return MealServiceResponse(**row[0])

    @classmethod
    def request_school_info(cls, params: RequestParameters) -> SchoolInfoResponse:
        row = cls._get_requests(url=cls.BASE_URL + SubUrl.INFO,
                                service_name=SubUrl.INFO,
                                params=params)
        return SchoolInfoResponse(**row[0])

    @classmethod
    def request_elementary_time_table(cls, params: RequestParameters) -> TimeTableResponse[ElementaryTimeTableRow]:
        rows = cls._get_requests(url=cls.BASE_URL + SubUrl.ELEMENTARY_TIME_TABLE,
                                 service_name=SubUrl.ELEMENTARY_TIME_TABLE,
                                 params=params)
        return TimeTableResponse([ElementaryTimeTableRow(**row) for row in rows])

    @classmethod
    def request_middle_time_table(cls, params: RequestParameters) -> TimeTableResponse[MiddleTimeTableRow]:
        rows = cls._get_requests(url=cls.BASE_URL + SubUrl.MIDDLE_TIME_TABLE,
                                 service_name=SubUrl.MIDDLE_TIME_TABLE,
                                 params=params)
        return TimeTableResponse([MiddleTimeTableRow(**row) for row in rows])

    @classmethod
    def request_high_time_table(cls, params: RequestParameters) -> TimeTableResponse[HighTimeTableRow]:
        rows = cls._get_requests(url=cls.BASE_URL + SubUrl.HIGH_TIME_TABLE,
                                 service_name=SubUrl.HIGH_TIME_TABLE,
                                 params=params)
        return TimeTableResponse([HighTimeTableRow(**row) for row in rows])

    @classmethod
    def request_school_schedule(cls, params: RequestParameters) -> SchoolScheduleResponse:
        rows = cls._get_requests(url=cls.BASE_URL + SubUrl.SCHOOL_SCHEDULE,
                                 service_name=SubUrl.SCHOOL_SCHEDULE,
                                 params=params)
        return SchoolScheduleResponse([SchoolScheduleRow(**row) for row in rows])

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
        if status_code == "INFO-000":
            return
        else:
            raise StatusCodeError(error_code=status_code)

    @classmethod
    def _get_row_data(cls, json_response: dict, service_name: str) -> dict:
        return json_response[service_name][1]["row"]
