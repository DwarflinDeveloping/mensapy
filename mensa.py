from dataclasses import dataclass
from enum import IntEnum
from typing import Optional


class Mensa(IntEnum):
    # Jena
    MENSA_ERNST_ABBE_PLATZ = 41
    MENSA_CARL_ZEISS_PROMENADE = 58
    MENSA_PHILOSOPHENWEG = 59
    MENSA_UNI_HAUPTGEBAUDE = 64
    MENSA_MORITZ_VON_ROHR_STRASSE = 61
    CAFETERIA_CARL_ZEISS_STRASSE = 62

    # Erfurt
    MENSA_NORDHAUSER_STRASSE = 44
    MENSA_ALTONAER_STRASSE = 47
    CAFETERIA_SCHLUTERSTRASSE = 51
    CAFETERIA_LEIPZIGER_STRASSE = 52

    # Ilmenau
    MENSA_EHRENBERG = 46
    CAFETERIA_MENSA_EHRENBERG = 53
    CAFETERIA_NANOTERIA = 55
    CAFETERIA_ROENTGENBAU = 57

    # Gera
    MENSA_WEG_DER_FREUNDSCHAFT = 67

    # Eisenach
    MENSA_AM_WARTENBERG = 69

    # Nordhausen
    MENSA_WEINBERGHOF = 71

    # Schmalkalden
    MENSA_BLECHHAMMER = 73

    # Weimar
    MENSA_AM_PARK = 77
    CAFETERIA_AM_HORN = 76
    CAFETERIA_MENSA_AM_PARK = 78


@dataclass
class Meal:
    name: str
    gebinde: int
    rscid: int
    proddat: str
    symbols: str
    likes: Optional[int]
    zusatzstoffe: Optional[str]
    allergene: Optional[list[str]]
    komponenten: Optional[list[str]]
    tooltip: Optional[list[str]]
    co2_equivalent: Optional[int]
    price_student: Optional[float]
    price_bedienstet: Optional[float]
    price_gast: Optional[float]
