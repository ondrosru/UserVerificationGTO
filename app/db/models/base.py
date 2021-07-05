import re
from typing import Any
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", '_', cls.__name__).lower()


Base = declarative_base(cls=CustomBase)
