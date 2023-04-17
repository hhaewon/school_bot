import os
from dataclasses import dataclass, field, asdict
from typing import Optional

from libs.api.responses.TimeTableResponse import T, ElementaryTimeTableRow, MiddleTimeTableRow, HighTimeTableRow
from libs.SubUrl import SubUrl


time_table_classes: dict[str, type[T]] = {
    SubUrl.ELEMENTARY.name: ElementaryTimeTableRow,
    SubUrl.MIDDLE.name: MiddleTimeTableRow,
    SubUrl.HIGH.name: HighTimeTableRow,
}


@dataclass(slots=True, kw_only=True)
class RequestParameters:
    """
    Attributes:
        SCHUL_NM: 학교명
        ATPT_OFCDC_SC_CODE: 시도교육청 코드
        KEY: 인증
        Type: 호출 문서(xml, json)
        pIndex: 페이지 위치
        pSize: 페이지 당 신청 숫자
        SD_SCHUL_CODE: 표준 학교 코드
        MMEAL_SC_CODE: 식사코드 (1: 조식, 2: 중식, 3: 석식)
        MLSV_YMD: 급식 일자
        MLSV_FROM_YMD: 급식 시작 일자
        MLSV_TO_YMD: 급식 종료 일자
        ALL_TI_YMD: 시간표일자
        GRADE: 학년
        CLASS_NM: 반명
        TI_FROM_YMD: 시간표 시작 일자
        TI_TO_YMD: 시간표 종료 일자
        AA_YMD: 학사일자
        AA_FROM_YMD: 학사시작일자
        AA_TO_YMD: 학사종료일자
    """
    SCHUL_NM: str
    ATPT_OFCDC_SC_CODE: str
    KEY: str = field(init=False, repr=False, default=os.environ['NEIS_TOKEN'])
    Type: str = field(init=False, repr=False, default='json')
    pIndex: int = 1
    pSize: int = 1000
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
    AA_YMD: Optional[str] = None
    AA_FROM_YMD: Optional[str] = None
    AA_TO_YMD: Optional[str] = None
    school_level: SubUrl = field(init=False, repr=False)

    def asdict_without_None(self) -> dict[str, str]:
        return asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})

    def __post_init__(self):
        if self.SCHUL_NM.endswith("초등학교"):
            self.school_level = SubUrl.ELEMENTARY
        elif self.SCHUL_NM.endswith("중학교"):
            self.school_level = SubUrl.MIDDLE
        elif self.SCHUL_NM.endswith("고등학교"):
            self.school_level = SubUrl.HIGH
        else:
            raise ValueError("school name is not available")
