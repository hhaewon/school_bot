import json
from dataclasses import asdict

import requests

from api.RequestParameters import RequestParameters
from api.error import StatusCodeError


class Request:
    @classmethod
    def get_requests(cls, url: str, params: RequestParameters) -> dict:
        service_name = url.split("/")[-1]

        response = requests.get(url=url, params=params.asdict_ignoring_none())
        response.encoding = "UTF-8"

        text = response.text.replace("<br/>", "\n")
        json_response = cls._loads_json(json_string=text)
        status_code = cls._get_status_code(json_response=json_response, key=service_name)
        cls._check_status_code(status_code=status_code)

        return cls._get_row_data(json_response=json_response,
                                 service_name=service_name,
                                 office_education_name=params.ATPT_OFCDC_SC_NM)

    @classmethod
    def _loads_json(cls, json_string: str) -> dict:
        return json.loads(s=json_string, strict=False)

    @classmethod
    def _get_status_code(cls, json_response: dict, key: str) -> str:
        try:
            if isinstance(json_response[key][0]['head'], list):
                status_code = json_response[key][0]["head"][1]["RESULT"]["CODE"]
            else:
                status_code = json_response[key][0]["head"]["RESULT"]["CODE"]
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
    def _get_row_data(cls, json_response: str, service_name: str, office_education_name: str) -> dict:
        row_list = json_response[service_name][1]["row"]
        for row in row_list:
            if row['ATPT_OFCDC_SC_NM'] == office_education_name:
                return row
        raise ValueError("can't find school")



