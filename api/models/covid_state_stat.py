from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from api.models.base import Base


class CovidStateStat(Base):
    __tablename__ = "covid_state_stats"

    dt: Mapped[date] = mapped_column(name="date", primary_key=True)

    state: Mapped[str] = mapped_column(primary_key=True)

    death: Mapped[int] = mapped_column()

    death_confirmed: Mapped[int] = mapped_column()

    death_probable: Mapped[int] = mapped_column()

    hospitalized: Mapped[int] = mapped_column()

    hospitalized_cumulative: Mapped[int] = mapped_column()

    hospitalized_currently: Mapped[int] = mapped_column()

    hospitalized_increase: Mapped[int] = mapped_column()

    in_icu_cumulative: Mapped[int] = mapped_column()

    in_icu_currently: Mapped[int] = mapped_column()

    on_ventilator_cumulative: Mapped[int] = mapped_column()

    on_ventilator_currently: Mapped[int] = mapped_column()

    recovered: Mapped[int] = mapped_column()
