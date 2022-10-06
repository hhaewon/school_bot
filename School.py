import datetime
import json
from typing import Final

import requests

import utils


class School:
    BASE_URL: Final[str] = "https://open.neis.go.kr/hub/"

    def __init__(self, params: dict[RequestParams, str]) -> None:
        self.params: dict[RequestParams, str] = {
            RequestParams.KEY: utils.get_token('neis'),
            RequestParams.TYPE: "json",
            **params
        }
        self.school_info: dict[RequestParams, str] = dict()

        school_name: str = self.params[RequestParams.SCHOOL_NAME]
        if school_name.en_url = SubUrl.ELEMENTARY_SCHOOL_SCHEDULE
        elif school_name.endswith('중학교'):
            self.schedule_sub_url = SubUrl.MIDDLE_SCHOOL_SCHEDULE
        elif school_name.endswith('고등학교'):
            self.schedule_sub_url = SubUrl.HIGH_SCHOOL_SCHEDULE
        else:
            pass

    def get_data(self, sub_url: SubUrl):
        URL = SchoolApi.BASE_URL + sub_url
        self.params.update(self.school_info)

        response = requests.get(URL, params=self.params)
        json_response = json.loads(response.text)

        if "RESULT" in json_response.keys():
            raise ValueError("fail getting data")

        json_body = json_response[sub_url]

        if json_body[0]["head"][0]["list_total_count"] == 1:
            return json_body[1]["row"][0]
        else:
            return json_body[1]["row"]

    def set_school_info(self) -> None:
        datas = self.get_data(sub_url=SubUrl.INFO)
        data = None
        for row in datas:
            if row['ATPT_OFCDC_SC_NM'] == self.params[RequestParams.OFFICE_EDUCATION_NAME]:
                data = row

        if data is None:
            raise ValueError("can't find school")

        self.school_info = {
            RequestParams.OFFICE_EDUCATION_CODE: data["ATPT_OFCDC_SC_CODE"],
            RequestParams.SCHOOL_CODE: data["SD_SCHUL_CODE"]
        }

    def get_meal(self) -> str:
        try:
            data = self.get_data(sub_url=SubUrl.MEAL)
        except ValueError:
            return '오늘은 급식이 없습니다.'

        string = data["DDISH_NM"].replace("<br/>", "\n")
        characters = "1234567890.()"
        for x in range(len(characters)):
            string = string.replace(characters[x], "")
        return string

    def get_schedule(self) -> str:
        try:
            datas: list[dict[str, str]] = self.get_data(sub_url=self.schedule_sub_url)
        except ValueError:
            return '오늘은 시간표가 없습니다.'

        string = ""
        for index, data in enumerate(datas, 1):
            subject = data["ITRT_CNTNT"].replace('-', '')
            string += f'{index}교시 : {subject}\n'
        return string

    def send_kakao_message(self, date_string: str):
        date_format = datetime.datetime.strptime(date_string, "%Y%m%d")
        date = f"{date_format:%Y/%m/%d (%a)}"
        text = (
            f'{date}의 급식과 시간표\n'
            '-------------\n'
            '오늘의 급식\n'
            f"{self.get_meal()}\n"
            '--------------\n'
            '오늘의 시간표\n'
            f"{self.get_schedule()}"
        )
        Kakao().send_to_kakao(text=text)

