region_codes = {
    "서울": "B10",
    "부산": "C10",
    "대구": "D10",
    "인천": "E10",
    "광주": "F10",
    "대전": "G10",
    "울산": "H10",
    "세종": "I10",
    "경기": "J10",
    "강원": "K10",
    "충북": "M10",
    "충남": "N10",
    "전북": "P10",
    "전남": "Q10",
    "경북": "R10",
    "경남": "S10",
    "제주": "T10",
}

office_education_names = {v: i for i, v in region_codes.items()}


def get_region_code(office_education_name: str) -> str:
    return region_codes[office_education_name]


def get_office_education_name(region_code: str) -> str:
    return office_education_names[region_code]

