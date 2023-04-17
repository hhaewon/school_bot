from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class SchoolInfoResponse:
    """
    Attributes:
        ATPT_OFCDC_SC_CODE: 시도교육청코드\n
        ATPT_OFCDC_SC_NM: 시도교육청명\n
        SD_SCHUL_CODE: 표준학교코드\n
        SCHUL_NM: 학교명\n
        ENG_SCHUL_NM: 영문학교명\n
        SCHUL_KND_SC_NM: 학교종류명\n
        LCTN_SC_NM: 소재지명\n
        JU_ORG_NM: 관할조직명\n
        FOND_SC_NM: 설립명\n
        ORG_RDNZC: 도로명우편번호\n
        ORG_RDNMA: 도로명주소\n
        ORG_RDNDA: 도로명상세주소\n
        ORG_TELNO: 전화번호\n
        HMPG_ADRES: 홈페이지주소\n
        COEDU_SC_NM: 남녀공학구분명\n
        ORG_FAXNO: 팩스번호\n
        HS_SC_NM: 고등학교구분명\n
        INDST_SPECL_CCCCL_EXST_YN: 산업체특별학급존재여부\n
        HS_GNRL_BUSNS_SC_NM: 고등학교일반실업구분명\n
        SPCLY_PURPS_HS_ORD_NM: 특수목적고등학교계열명\n
        ENE_BFE_SEHF_SC_NM: 입시전후기구분명\n
        DGHT_SC_NM: 주야구분명\n
        FOND_YMD: 설립일자\n
        FOAS_MEMRD: 개교기념일\n
        LOAD_DTM: 수정일\n
    """
    ATPT_OFCDC_SC_CODE: str
    ATPT_OFCDC_SC_NM: str
    SD_SCHUL_CODE: str
    SCHUL_NM: str
    ENG_SCHUL_NM: str
    SCHUL_KND_SC_NM: str
    LCTN_SC_NM: str
    JU_ORG_NM: str
    FOND_SC_NM: str
    ORG_RDNZC: str
    ORG_RDNMA: str
    ORG_RDNDA: str
    ORG_TELNO: str
    HMPG_ADRES: str
    COEDU_SC_NM: str
    ORG_FAXNO: str
    HS_SC_NM: str
    INDST_SPECL_CCCCL_EXST_YN: str
    HS_GNRL_BUSNS_SC_NM: str
    SPCLY_PURPS_HS_ORD_NM: str
    ENE_BFE_SEHF_SC_NM: str
    DGHT_SC_NM: str
    FOND_YMD: str
    FOAS_MEMRD: str
    LOAD_DTM: str
