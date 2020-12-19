from enum import unique, Enum
from typing import Tuple


@unique
class TicketSource(Enum):
    cc1551 = 'cc1551'  # tickets parsed from 1551.gov.ua
    api = 'api'  # tickets created by API


@unique
class TicketStatus(Enum):
    new = 'На модерації'
    active = 'В роботі'
    finished = 'Звернення виконано'

    @classmethod
    def get_values(cls) -> Tuple[str, ...]:
        return tuple(cls.__members__.values())


@unique
class TicketPriority(Enum):
    discomfort = 'discomfort'
    waiting = 'waiting'
    losing_money = 'losing_money'
    damage = 'damage'
    death = 'death'
