import enum
from abc import ABC
from typing import Any, Optional, Type

import sqlalchemy as sa


class SoftEnum(sa.TypeDecorator):
    impl = sa.Text

    def __init__(
        self,
        _enum: Optional[Type[enum.Enum]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        self._enum = _enum
        super().__init__(*args, **kwargs)

    def process_bind_param(
        self,
        enum_: enum.Enum,
        dialect: Any,
    ) -> Optional[str]:
        if enum_ is None:
            return None
        return enum_.value
