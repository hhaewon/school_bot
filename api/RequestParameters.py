from dataclasses import dataclass, field
from typing import Optional

from utils import get_token


@dataclass(slots=True)
class RequestParameters:
    """
    SCHUL_NM: 학교명\n
    ATPT_OFCDC_SC_CODE: 시도교육청 코드\n
    KEY: 인증키\n
    Type: 호출 문서(xml, json)\n
    pIndex: 페이지 위치\n
    pSize: 페이지 당 신청 숫자\n
    SD_SCHUL_CODE: 표준 학교 코드\n
    MMEAL_SC_CODE: 식사코드 (1: 조식, 2: 중식, 3: 석식)\n
    MLSV_YMD: 급식 일자\n
    MLSV_FROM_YMD: 급식 시작 일자\n
    MLSV_TO_YMD: 급식 종료 일자\n
    ALL_TI_YMD: 시간표일자\n
    GRADE: 학년\n
    CLASS_NM: 반명\n
    TI_FROM_YMD: 시간표 시작 일자\n
    TI_TO_YMD: 시간표 종료 일자\n
    """
    SCHUL_NM: str
    ATPT_OFCDC_SC_CODE: str
    KEY: str = field(init=False, repr=False, default=get_token('neis'))
    Type: str = field(init=False, repr=False, default='json')
    pIndex: int = 1
    pSize: int = 100
    SD_SCHUL_CODE: Optional[str] = None
    MMEAL_SC_CODE: Optional[str] = None
    MLSV_YMD: Optional[str] = None
    MLSV_FROM_YMD: Optional[str] = None
    MLSV_TO_YMD: Optional[str] = None
    ALL_TI_YMD: Optional[str] = None
    GRADE: Optional[str] = None
    CLASS_NM: Optional[str] = None
    TI_FROM_YMD: Optional[str] = None
    TI_TO_YMD: Optional[str] = None


