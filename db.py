from sqlalchemy.orm import (
    DeclarativeBase,
    scoped_session,
    sessionmaker,
    Mapped,
    mapped_column,
    relationship,
    Session,
    Query,
)
from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Date,
    Time,
    ForeignKey,
)
from datetime import date, time, datetime
from typing import Union, Self

from config import DB_URL
from weekdays import WEEKDAY_ALIASES

__all__ = (
    'Base',
    'User',
    'WeekDay',
    'TimeWindow',
)


class Base(DeclarativeBase):

    _engine = create_engine(url=DB_URL)
    _session = scoped_session(
        sessionmaker(autocommit=False,
                     autoflush=False,
                     expire_on_commit=False,
                     bind=_engine,
                     )
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    def get_session(cls) -> scoped_session[Session]:
        return cls._session

    @classmethod
    def reset_db(cls) -> None:
        cls.metadata.create_all(cls._engine)

    @classmethod
    def _query(cls) -> Query:
        return cls._session.query(cls)

    @classmethod
    def all(cls) -> list[Self]:
        return cls._session.query(cls).all()  # type: ignore

    @classmethod
    def by_id(cls, id_: int) -> Self:
        return cls._query().filter(cls.id == id_).first()

    @classmethod
    def exists(cls, id_: int) -> bool:
        return bool(cls._query().filter(cls.id == id_).first())


class User(Base):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String, nullable=False)
    room: Mapped[int] = mapped_column(Integer, nullable=True)

    time_windows: Mapped[list['TimeWindow']] = relationship(
        back_populates='user',
        cascade='all, delete',
        lazy='dynamic',
    )

    @property
    def records_count(self) -> int:
        return self.time_windows.count()


class WeekDay(Base):
    __tablename__ = 'weekdays'

    value: Mapped[int] = mapped_column(Integer, nullable=False)

    time_windows: Mapped[list['TimeWindow']] = relationship(
        back_populates='weekday',
        cascade='all, delete',
        lazy='dynamic',
    )

    _WEEKDAY_ALIASES = WEEKDAY_ALIASES

    @classmethod
    def get(cls, weekday_index: int) -> Self:
        return cls._session.query(cls).filter(cls.value == weekday_index).first()

    @classmethod
    def all_sorted(cls) -> list[Self]:
        cur_weekday: int = datetime.now().weekday()
        return sorted(cls.all(), key=lambda x: 0 if x.value >= cur_weekday else 1)

    @property
    def text(self) -> str:
        return self._WEEKDAY_ALIASES[self.value]


class TimeWindow(Base):
    __tablename__ = 'time_windows'

    weekday_id: Mapped[int] = mapped_column(ForeignKey('weekdays.id'), nullable=False)

    date: Mapped[date] = mapped_column(Date, nullable=False)
    start: Mapped[time] = mapped_column(Time, nullable=False)
    end: Mapped[time] = mapped_column(Time, nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)

    weekday: Mapped['WeekDay'] = relationship(back_populates='time_windows', uselist=False)
    user: Mapped[Union['User', None]] = relationship(back_populates='time_windows', uselist=False)

    @property
    def text(self) -> str:
        time_str = f'{self.start.strftime("%H:%M")} - {self.end.strftime("%H:%M")}'
        date_str = f' ({self.date.strftime("%d.%m")})'
        return time_str + date_str

    @property
    def taken(self) -> bool:
        return bool(self.user_id)
