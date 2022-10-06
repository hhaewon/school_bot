from SubUrl import SubUrl
from api.RequestParameters import RequestParameters
from api.SchoolLevel import SchoolLevel
from api.request import Request


class SchoolApi:
    BASE_URL = "https://open.neis.go.kr/hub/"

    @classmethod
    def load_school_info(cls, params: RequestParameters):
        URL = cls.BASE_URL + SubUrl.INFO.value
        return Request.get_requests(url=URL, params=params)


    @classmethod
    def load_meal_service(cls, params: RequestParameters):
        URL = cls.BASE_URL + SubUrl.MEAL.value
        return Request.get_requests(url=URL, params=params)

    @classmethod
    def load_time_table(cls, school_level: SchoolLevel, params: RequestParameters):
        URL = cls.BASE_URL + SchoolLevel.value
        return Request.get_requests(url=URL, params=params)

