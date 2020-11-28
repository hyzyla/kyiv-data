from dataclasses import dataclass


@dataclass(frozen=True)
class UserCtx:
    user_id: str
    token: str
