from dataclasses import dataclass
from enum import Enum
import re
from typing import List


@dataclass(init=True, frozen=True)
class TariffInformation:
    date: str
    base_rate: float
    domestic_first_rate: float
    domestic_second_rate: float
    domestic_third_rate: float
    business_rate: float
    sports_rate: float
    public_rate: float
    low_voltage_rate: float
    high_voltage_rate: float


class TariffCategory(Enum):
    DOMESTIC = "PCD"
    BUSINESS = "TUP"
    SPORTS = "T"
    PUBLIC = "EP"
    LOW_VOLTAGE = "TU"
    HIGH_VOLTAGE = "MT"


def find_index_of_category(category: TariffCategory, lines: List[str]) -> int:
    index = next((i for i, l in enumerate(lines) if f"({category.value})" in l), -1)
    if index == -1:
        raise ValueError(f"Could not find index of {category.name} tariff category")
    return index


def extract_vatu_amount(line):
    l = line.strip().lower()
    return float(re.search("\d{2,3},\d{2} vatu", l).group().replace(",", ".")[:-5])


def extract_tariff_information(lines: List[str]):
    base_rate = extract_vatu_amount(lines[0])
    index = find_index_of_category(TariffCategory.DOMESTIC, lines)
    domestic_first_rate = extract_vatu_amount(lines[index + 2])
    domestic_second_rate = extract_vatu_amount(lines[index + 3])
    domestic_third_rate = extract_vatu_amount(lines[index + 4])
    index = find_index_of_category(TariffCategory.BUSINESS, lines)
    business_rate = extract_vatu_amount(lines[index + 1])
    index = find_index_of_category(TariffCategory.SPORTS, lines)
    sports_rate = extract_vatu_amount(lines[index + 1])
    index = find_index_of_category(TariffCategory.PUBLIC, lines)
    public_rate = extract_vatu_amount(lines[index + 1])
    index = find_index_of_category(TariffCategory.LOW_VOLTAGE, lines)
    low_voltage_rate = extract_vatu_amount(lines[index + 1])
    index = find_index_of_category(TariffCategory.HIGH_VOLTAGE, lines)
    high_voltage_rate = extract_vatu_amount(lines[index + 1])
    return dict(
        base_rate=base_rate,
        domestic_first_rate=domestic_first_rate,
        domestic_second_rate=domestic_second_rate,
        domestic_third_rate=domestic_third_rate,
        business_rate=business_rate,
        sports_rate=sports_rate,
        public_rate=public_rate,
        low_voltage_rate=low_voltage_rate,
        high_voltage_rate=high_voltage_rate,
    )

