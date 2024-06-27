from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

# A maneira de fazer isso pelo registry com decorator é mais sucinta
# Ver isso em: https://docs.sqlalchemy.org/en/20/orm/dataclasses.html

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, nullable=True, onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f'User(id={self.id}, name={self.username})'
