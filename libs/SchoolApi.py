import json

import aiohttp

from .SubUrl import SubUrl
from .responses.MealServiceResponse import MealServiceResponse
from .responses.SchoolInfoResponse import SchoolInfoResponse
from .responses.SchoolScheduleResponse import SchoolScheduleResponse, SchoolScheduleRow
from .responses.TimeTableResponse import TimeTableResponse, T
from .RequestParameters import RequestParameters, time_table_classes
from .StatusCodeError import StatusCodeError


class SchoolApi:
    BASE_URL = "https://open.neis.go.kr/hub/"

    @classmethod
    async def _get_requests(cls, url: str, service_name: str, params: RequestParameters) -> dict:
        async with (aiohttp.ClientSession() as session,
                    session.get(url=url, params=params.asdict_without_None()) as response):
            text = (await response.text()).replace("<br/>", "\n")
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

    @classmethod
    async def request_meal_service(cls, params: RequestParameters) -> MealServiceResponse:
        row = await cls._get_requests(url=cls.BASE_URL + SubUrl.MEAL,
                                      service_name=SubUrl.MEAL,
                                      params=params)
        return MealServiceResponse(**row[0])

    @classmethod
    async def request_school_info(cls, params: RequestParameters) -> SchoolInfoResponse:
        row = await cls._get_requests(url=cls.BASE_URL + SubUrl.INFO,
                                      service_name=SubUrl.INFO,
                                      params=params)
        return SchoolInfoResponse(**row[0])

    @classmethod
    async def request_time_table(cls, params: RequestParameters) -> TimeTableResponse[T]:
        response_type = time_table_classes[params.school_level.name]
        rows = await cls._request_time_table(params=params, response_type=response_type)
        return rows

    @classmethod
    async def _request_time_table(cls, params: RequestParameters, response_type: type[T]) -> TimeTableResponse[T]:
        sub_url = getattr(SubUrl, params.school_level.name)
        rows = await cls._get_requests(url=f"{cls.BASE_URL}{sub_url}",
                                       service_name=sub_url,
                                       params=params)

        return TimeTableResponse([response_type(**row) for row in rows])

    @classmethod
    async def request_school_schedule(cls, params: RequestParameters) -> SchoolScheduleResponse:
        rows = await cls._get_requests(url=cls.BASE_URL + SubUrl.SCHOOL_SCHEDULE,
                                       service_name=SubUrl.SCHOOL_SCHEDULE,
                                       params=params)
        return SchoolScheduleResponse([SchoolScheduleRow(**row) for row in rows])
