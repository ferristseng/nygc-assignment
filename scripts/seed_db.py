import csv
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from pathlib import Path


class Base(DeclarativeBase):
    pass


class CrimeData(Base):
    __tablename__ = "crime_data"

    case_number: Mapped[str] = mapped_column()

    unique_key: Mapped[str] = mapped_column(primary_key=True)

    date: Mapped[datetime] = mapped_column()

    block: Mapped[str] = mapped_column()

    beat: Mapped[str] = mapped_column()

    ward: Mapped[str] = mapped_column()

    community_area: Mapped[str] = mapped_column()

    primary_type: Mapped[str] = mapped_column()

    description: Mapped[str] = mapped_column()

    location_description: Mapped[str] = mapped_column()

    arrest: Mapped[bool] = mapped_column()

    latitude: Mapped[Optional[float]] = mapped_column()

    longitude: Mapped[Optional[float]] = mapped_column()


input_csv = Path("data/crime.csv")  # 113M


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"


def convert_dt(value: str) -> datetime:
    parsed_date = datetime.strptime(value, DATETIME_FORMAT)
    # TODO: Not sure if this should support other timezones
    parsed_date = parsed_date.replace(tzinfo=timezone.utc)
    return parsed_date


def convert_float(value: Optional[str]) -> Optional[float]:
    if not value:
        return None

    return float(value)


if __name__ == "__main__":
    load_dotenv(".env")

    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/{db_name}"
    )

    Base.metadata.create_all(engine)

    session = Session(engine, autoflush=True)

    with engine.connect() as connection:
        count = 0
        with open(input_csv, mode="r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                converted_row = CrimeData(
                    case_number=row["case_number"],
                    unique_key=row["unique_key"],
                    date=convert_dt(row["date"]),
                    block=row["block"],
                    beat=row["beat"],
                    ward=row["ward"],
                    community_area=row["community_area"],
                    primary_type=row["primary_type"],
                    description=row["description"],
                    location_description=row["location_description"],
                    arrest=bool(True if row["arrest"] == "true" else False),
                    latitude=convert_float(row.get("latitude")),
                    longitude=convert_float(row.get("longitude")),
                )
                session.add(converted_row)
                session.commit()
                print(f"Added {count} arrest={row['arrest']}")
                count += 1
