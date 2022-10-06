from dataclasses import dataclass, field, asdict
from typing import Optional

from utils import get_token


@dataclass(slots=True)
class RequestParameters:
    ATPT_OFCDC_SC_NM: str = field(repr=False)
    SCHUL_NM: str
    KEY: str = field(init=False, repr=False, default=get_token('neis'))
    Type: str = field(init=False, repr=False, default='json')
    pIndex: int = 1
    pSize: int = 100
    ATPT_OFCDC_SC_CODE: Optional[str] = None
    SD_SCHUL_CODE: Optional[str] = None
    MMEAL_SC_CODE: Optional[str] = None
    MLSV_YMD: Optional[str] = None
    MLSV_FROM_YMD: Optional[str] = None
    MLSV_TO_YMD: Optional[str] = None

    def asdict_ignoring_none(self):
        return asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})