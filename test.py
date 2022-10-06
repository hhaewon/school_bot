import unittest

from api.RequestParameters import RequestParameters
from api.SchoolApi import SchoolApi


class TestApi(unittest.TestCase):
    params = RequestParameters(
            SCHUL_NM="반곡중학교",
            ATPT_OFCDC_SC_NM="강원도교육청",
    )

    def test_get_school_info(self):
        response = SchoolApi.load_school_info(params=TestApi.params)
        self.assertIsNotNone(response)




