from dataclasses import dataclass, field, asdict
from typing import Optional

from utils import get_token


@dataclass(slots=True)
class RequestParameters:
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

