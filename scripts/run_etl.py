import csv
import json
import logging
import os
import sys
from time import perf_counter
from typing_extensions import Annotated
from pydantic import BaseModel, BeforeValidator
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional
from pathlib import Path

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel("INFO")

# Is 24H time correct here?
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"


def dt_validator(value: str) -> datetime:
    parsed_date = datetime.strptime(value, DATETIME_FORMAT)
    # TODO: Not sure if this should support other timezones
    parsed_date = parsed_date.replace(tzinfo=timezone.utc)
    return parsed_date


def float_validator(value: Optional[str]) -> Optional[float]:
    if not value:
        return None

    return float(value)


DateTime = Annotated[datetime, BeforeValidator(dt_validator)]
Coordinate = Annotated[Optional[float], BeforeValidator(float_validator)]


class CrimeDataRecord(BaseModel):
    unique_key: str
    case_number: str
    date: DateTime
    block: str
    primary_type: str
    description: str
    location_description: str
    arrest: bool
    latitude: Coordinate
    longitude: Coordinate

    class Config:
        json_encoders = {datetime: lambda v: v.strftime(DATETIME_FORMAT)}

    def to_json(self) -> dict:
        return self.model_dump(mode="json")


class CrimeTypeMetrics(BaseModel):
    primary_type: str
    arrest_count: int  # The count of all CrimeDataRecords for a primary_type where arrest == True.
    non_arrest_count: int  # The count of all CrimeDataRecords for a primary_type where arrest == False.


input_csv = Path("data/crime.csv")  # 113M
outputs_dir = Path(".outputs")


def parse() -> list[CrimeTypeMetrics]:
    """YOUR CODE GOES IN THIS FUNCTION.

    Assignment:
        - Unzip the data from crime.csv.gz to "data/crime.csv" (this does not have to be done in Python).
        - Update this parse() function to:
            - Read the data from "data/crime.csv" and parse all the data rows into the CrimeDataRecord class above.
            - Convert each CrimeDataRecord to JSON and output it to a corresponding text file in a directory called ".outputs".
            Each JSON string should be written to a single line in the corresponding file. The model has a ".to_json()" method
            to simplify conversion for you. Example:
                - outputs/
                    - PUBLIC PEACE VIOLATION.txt
                    - DECEPTIVE PRACTICE.txt
                    - CRIMINAL DAMAGE.txt
                    - NARCOTICS.txt
                    - etc...
            - Return a list of CrimeTypeMetric values, sorted from most frequently occurring to least.
                Occurrences should be calculated based on the number of CrimeTypeData records corresponding to the primary_type.

    Success Criteria:
        - Running this python module executes the parsing logic and test logic successfully without any errors.

    Additional Notes:
        - You may use any third party libraries or tools to execute this task but the entrypoint to the ETL process
        must be executed by Python. You should be able to explain and justify your choices during review.
        - First focus on getting the right solution and then focus on optimizations, like reducing the number of times the
        file is read or the number of times the row items are iterated over or the number of records kept in memory.
        Even if you choose not to make those optimizations, it'll still be good to have a discussion about what could have
        been done.
    """
    # Buffer for converted records. Primary Type => [CrimeDataRecord]
    buffer: dict[str, [CrimeDataRecord]] = {}

    # Tracking metrics. Primary Type => CrimeTypeMetrics
    metrics: dict[str, CrimeTypeMetrics] = {}

    # Read data into buffer.
    # Q: What happens if file is bigger than memory?
    with open(input_csv, mode="r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            converted_row = CrimeDataRecord(**row)

            if converted_row.primary_type not in buffer:
                buffer[converted_row.primary_type] = []
                metrics[converted_row.primary_type] = CrimeTypeMetrics(
                    primary_type=converted_row.primary_type,
                    arrest_count=0,
                    non_arrest_count=0,
                )

            buffer[converted_row.primary_type].append(converted_row)

            # Update metrics
            if converted_row.arrest:
                metrics[converted_row.primary_type].arrest_count += 1
            else:
                metrics[converted_row.primary_type].non_arrest_count += 1

    try:
        os.mkdir(outputs_dir)
    except FileExistsError:
        pass

    for primary_type, crime_records in buffer.items():
        with open(outputs_dir.joinpath(f"{primary_type}.txt"), "w+") as out_file:
            for record in crime_records:
                json.dump(record.to_json(), out_file)
                out_file.write("\n")

    ordered = sorted(
        metrics.values(),
        key=lambda metric: metric.arrest_count + metric.non_arrest_count,
        reverse=True,
    )

    return ordered


def check_criteria(test: Callable, name: str):
    """DO NOT CHANGE THIS."""

    try:
        test()
        logger.info(f"Test [{name}]: PASSED")
    except:
        logger.error(f"Test [{name}]: FAILED")
        raise


def test_crime_type_ordering(crime_metrics: list[CrimeTypeMetrics]):
    """DO NOT CHANGE THIS."""

    expected_ordered_crime_metrics = [
        ["THEFT", 9689, 96847],
        ["BATTERY", 19514, 67270],
        ["CRIMINAL DAMAGE", 3586, 55385],
        ["ASSAULT", 7432, 28653],
        ["BURGLARY", 1823, 32026],
        ["OTHER OFFENSE", 4851, 27937],
        ["DECEPTIVE PRACTICE", 4381, 24413],
        ["NARCOTICS", 27876, 284],
        ["MOTOR VEHICLE THEFT", 2123, 25239],
        ["ROBBERY", 1924, 15515],
        ["CRIMINAL TRESPASS", 7687, 4812],
        ["OFFENSE INVOLVING CHILDREN", 1033, 4727],
        ["WEAPONS VIOLATION", 3799, 1812],
        ["PUBLIC PEACE VIOLATION", 2293, 2035],
        ["SEX OFFENSE", 958, 2137],
        ["CRIM SEXUAL ASSAULT", 429, 1860],
        ["LIQUOR LAW VIOLATION", 1583, 11],
        ["ARSON", 211, 1154],
        ["PROSTITUTION", 1323, 6],
        ["KIDNAPPING", 106, 1051],
        ["INTERFERENCE WITH PUBLIC OFFICER", 933, 126],
        ["GAMBLING", 872, 6],
        ["HOMICIDE", 389, 340],
        ["INTIMIDATION", 97, 445],
        ["STALKING", 80, 427],
        ["CRIMINAL SEXUAL ASSAULT", 24, 260],
        ["OBSCENITY", 71, 20],
        ["CONCEALED CARRY LICENSE VIOLATION", 38, 0],
        ["NON-CRIMINAL", 1, 17],
        ["OTHER NARCOTIC VIOLATION", 15, 3],
        ["PUBLIC INDECENCY", 18, 0],
        ["HUMAN TRAFFICKING", 1, 8],
        ["NON - CRIMINAL", 2, 5],
        ["RITUALISM", 0, 5],
        ["NON-CRIMINAL (SUBJECT SPECIFIED)", 1, 1],
    ]
    assert len(crime_metrics) == len(
        expected_ordered_crime_metrics
    ), "The list of metrics do not match the expected count."
    for i in range(0, len(crime_metrics)):
        assert (
            crime_metrics[i].primary_type == expected_ordered_crime_metrics[i][0]
        ), f"The metric at output index {i} did not match the expected value"
        assert (
            crime_metrics[i].arrest_count == expected_ordered_crime_metrics[i][1]
        ), f"The metric at output index {i} did not match the expected value"
        assert (
            crime_metrics[i].non_arrest_count == expected_ordered_crime_metrics[i][2]
        ), f"The metric at output index {i} did not match the expected value"


def test_output_files(output_path: Path):
    """DO NOT CHANGE THIS."""

    assert output_path.exists(), "The .outputs directory is missing."
    assert output_path.is_dir(), "The .outputs directory is missing."

    for file in output_path.glob("*.txt"):
        primary_type = file.name[: len(file.name) - 4]

        with open(file, "r") as file_handle:
            for line in file_handle:
                record = CrimeDataRecord.parse_raw(line)
                assert (
                    record.primary_type == primary_type
                ), f"The record with crime type {record.primary_type} does not belong in this file of {primary_type} records."


if __name__ == "__main__":
    """DO NOT CHANGE THIS."""

    logger.info("Executing parse() method.")
    t1 = perf_counter()
    output = parse()
    t2 = perf_counter()
    logger.info(f"Completed parsing in {timedelta(seconds=t2-t1)}.")

    check_criteria(
        lambda: test_crime_type_ordering(crime_metrics=output),
        "Crime type metrics are aggregated and sorted by frequency",
    )
    check_criteria(
        lambda: test_output_files(output_path=outputs_dir),
        "Output files are grouped by crime type",
    )
