from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True, kw_only=True)
class SchoolScheduleRow:
    """
    ATPT_OFCDC_SC_CODE: 시도교육청코드
    ATPT_OFCDC_SC_NM: 시도교육청명
    SD_SCHUL_CODE: 표준학교코드
    SCHUL_NM: 학교명
    AY: 학년도
    DGHT_CRSE_SC_NM: 주야과정명
    SCHUL_CRSE_SC_NM: 학교과정명
    SBTR_DD_SC_NM: 수업공제일명
    AA_YMD: 학사일자
    EVENT_NM: 행사명
    EVENT_CNTNT: 행사내용
    ONE_GRADE_EVENT_YN: 1학년행사여부
    TW_GRADE_EVENT_YN: 2학년행사여부
    THREE_GRADE_EVENT_YN: 3학년행사여부
    FR_GRADE_EVENT_YN: 4학년행사여부
    FIV_GRADE_EVENT_YN: 5학년행사여부
    SIX_GRADE_EVENT_YN: 6학년행사여부
    LOAD_DTM: 수정일
    """
    ATPT_OFCDC_SC_CODE: str
    ATPT_OFCDC_SC_NM: str
    SD_SCHUL_CODE: str
    SCHUL_NM: str
    AY: str
    DGHT_CRSE_SC_NM: str
    SCHUL_CRSE_SC_NM: str
    SBTR_DD_SC_NM: str
    AA_YMD: str
    EVENT_NM: str
    EVENT_CNTNT: str
    ONE_GRADE_EVENT_YN: str
    TW_GRADE_EVENT_YN: str
    THREE_GRADE_EVENT_YN: str
    FR_GRADE_EVENT_YN: str
    FIV_GRADE_EVENT_YN: str
    SIX_GRADE_EVENT_YN: str
    LOAD_DTM: str


class SchoolScheduleResponse:
    def __init__(self, rows: Iterable[SchoolScheduleRow]):
        self.rows = rows

    @property
    def schedule(self) -> dict[str, str]:
        schedule_dict = dict()
        for row in self.rows:
            row.EVENT_NM = row.EVENT_NM.strip()
            if row.EVENT_NM == '토요휴업일':
                continue
            if row.EVENT_NM in ['여름방학', '겨울방학']:
                if row.EVENT_NM not in schedule_dict:
                    schedule_dict[row.EVENT_NM] = f'{self._format_date(row.AA_YMD)} ~ {self._format_date(row.AA_YMD)}'
                else:
                    schedule_dict[
                        row.EVENT_NM] = f'{schedule_dict[row.EVENT_NM][:10]} ~ {row.AA_YMD[:4]}/{row.AA_YMD[4:6]}/{row.AA_YMD[6:8]}'
            else:
                schedule_dict[row.EVENT_NM] = self._format_date(row.AA_YMD)
                # f'{row.AA_YMD[:4]}/{row.AA_YMD[4:6]}/{row.AA_YMD[6:8]}'

        return schedule_dict

    @staticmethod
    def _format_date(date: str):
        return f'{date[:4]}/{date[4:6]}/{date[6:8]}'

    def __repr__(self):
        return self.rows.__repr__()
