region_codes = {
    "서울특별시교육청": "B10",
    "부산광역시교육청": "C10",
    "대구광역시교육청": "D10",
    "인천광역시교육청": "E10",
    "광주광역시교육청": "F10",
    "대전광역시교육청": "G10",
    "울산광역시교육청": "H10",
    "세종특별자치시교육청": "I10",
    "경기도교육청": "J10",
    "강원도교육청": "K10",
    "충청북도교육청": "M10",
    "충청남도교육청": "N10",
    "전라북도교육청": "P10",
    "전라남도교육청": "Q10",
    "경상북도교육청": "R10",
    "경상남도교육청": "S10",
    "제주특별자치도교육청": "T10",
}

office_education_names = {v: i for i, v in region_codes.items()}


def get_region_code(office_education_name: str) -> str:
    return region_codes[office_education_name]


def get_office_education_name(region_code: str) -> str:
    return office_education_names[region_code]

