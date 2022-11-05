from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar, Sequence


@dataclass(kw_only=True, slots=True)
class ElementaryTimeTableRow:
    """
    ATPT_OFCDC_SC_CODE: 시도교육청코드\n
    ATPT_OFCDC_SC_NM: 시도교육청명\n
    SD_SCHUL_CODE: 표준학교코드\n
    SCHUL_NM: 학교명\n
    AY: 학년도\n
    SEM: 학기\n
    ALL_TI_YMD: 시간표일자\n
    GRADE: 학년\n
    CLASS_NM: 반명\n
    PERIO: 교시\n
    ITRT_CNTNT: 수업내용\n
    LOAD_DTM: 수정일\n
    """
    ATPT_OFCDC_SC_CODE: str
    ATPT_OFCDC_SC_NM: str
    SD_SCHUL_CODE: str
    SCHUL_NM: str
    AY: str
    SEM: str
    ALL_TI_YMD: str
    GRADE: str
    CLASS_NM: str
    PERIO: str
    ITRT_CNTNT: str
    LOAD_DTM: str


@dataclass(kw_only=True, slots=True)
class MiddleTimeTableRow:
    """
    ATPT_OFCDC_SC_CODE: 시도교육청코드
    ATPT_OFCDC_SC_NM: 시도교육청명
    SD_SCHUL_CODE: 표준학교코드
    SCHUL_NM: 학교명
    AY: 학년도
    SEM: 학기
    ALL_TI_YMD: 시간표일자
    DGHT_CRSE_SC_NM: 주야과정명
    GRADE: 학년
    CLASS_NM: 반명
    PERIO: 교시
    ITRT_CNTNT: 수업내용
    LOAD_DTM: 수정일
    """
    ATPT_OFCDC_SC_CODE: str
    ATPT_OFCDC_SC_NM: str
    SD_SCHUL_CODE: str
    SCHUL_NM: str
    AY: str
    SEM: str
    ALL_TI_YMD: str
    DGHT_CRSE_SC_NM: str
    GRADE: str
    CLASS_NM: str
    PERIO: str
    ITRT_CNTNT: str
    LOAD_DTM: str


@dataclass(kw_only=True, slots=True)
class HighTimeTableRow:
    """
    ATPT_OFCDC_SC_CODE: 시도교육청코드
    ATPT_OFCDC_SC_NM: 시도교육청명
    SD_SCHUL_CODE: 표준학교코드
    SCHUL_NM: 학교명
    AY: 학년도
    SEM: 학기
    ALL_TI_YMD: 시간표일자
    DGHT_CRSE_SC_NM: 주야과정명
    ORD_SC_NM: 계열명
    DDDEP_NM: 학과명
    GRADE: 학년
    CLRM_NM: 강의실명
    CLASS_NM: 반명
    PERIO: 교시
    ITRT_CNTNT: 수업내용
    LOAD_DTM: 수정일
    """
    ATPT_OFCDC_SC_CODE: str
    ATPT_OFCDC_SC_NM: str
    SD_SCHUL_CODE: str
    SCHUL_NM: str
    AY: str
    SEM: str
    ALL_TI_YMD: str
    DGHT_CRSE_SC_NM: str
    ORD_SC_NM: str
    DDDEP_NM: str
    GRADE: str
    CLRM_NM: str
    CLASS_NM: str
    PERIO: str
    ITRT_CNTNT: str
    LOAD_DTM: str


T = TypeVar('T', ElementaryTimeTableRow, MiddleTimeTableRow, HighTimeTableRow)


class TimeTableResponse(Generic[T]):
    def __init__(self, rows: Sequence[T]):
        self._rows: Sequence[T] = rows

    @property
    def time_table(self) -> list[str]:
        lst = []
        row: T
        for i, row in enumerate(self._rows, start=1):
            lst.append(f"{i}교시: {row.ITRT_CNTNT.replace('-', '')}")
        return lst

    @property
    def rows(self):
        return self._rows

    def __repr__(self):
        return self._rows.__repr__()
