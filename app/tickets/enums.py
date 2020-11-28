from enum import unique, Enum
from typing import Tuple


@unique
class TicketSource(Enum):
    cc1551 = 'cc1551'  # tickets parsed from 1551.gov.ua
    api = 'api'  # tickets created by API


@unique
class TicketStatus(Enum):
    active = 'В роботі'
    finished = 'Звернення виконано'

    @classmethod
    def get_values(cls) -> Tuple[str, ...]:
        return cls.active.value, cls.finished.value
