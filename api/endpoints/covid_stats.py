import subprocess
from typing import Optional
from datetime import date
from typing import Any
from api.db import get_session
from api.models.covid_state_stat import CovidStateStat
import json
from flask import Blueprint, request, Response
from sqlalchemy import and_
from pydantic import BaseModel, PositiveInt, Extra

blueprint = Blueprint("covid_stats", __name__, url_prefix="/covid-stats")


def stat_to_dict(stat: CovidStateStat) -> dict[str, Any]:
    as_dict = {
        "date": stat.dt,
        "state": stat.state,
        "death": stat.death,
        "death_confirmed": stat.death_confirmed,
        "death_probable": stat.death_probable,
        "hospitalized": stat.hospitalized,
        "hospitalized_cumulative": stat.hospitalized_cumulative,
        "hospitalized_currently": stat.hospitalized_currently,
        "hospitalized_increase": stat.hospitalized_increase,
        "in_icu_cumulative": stat.in_icu_cumulative,
        "in_icu_currently": stat.in_icu_currently,
        "on_ventilator_cumulative": stat.on_ventilator_cumulative,
        "on_ventilator_currently": stat.on_ventilator_currently,
        "recovered": stat.recovered,
    }
    return as_dict


def serialize_json_default(val: Any) -> str:
    if isinstance(val, date):
        return val.isoformat()

    raise TypeError("unserializable type")


class CovidStateStatUpdate(BaseModel):
    death_confirmed: Optional[PositiveInt] = None

    death_probable: Optional[PositiveInt] = None

    hospitalized: Optional[PositiveInt] = None

    hospitalized_cumulative: Optional[PositiveInt] = None

    hospitalized_currently: Optional[PositiveInt] = None

    hospitalized_increase: Optional[PositiveInt] = None

    in_icu_cumulative: Optional[PositiveInt] = None

    in_icu_currently: Optional[PositiveInt] = None

    on_ventilator_cumulative: Optional[PositiveInt] = None

    on_ventilator_currently: Optional[PositiveInt] = None

    recovered: Optional[PositiveInt] = None

    class Config:
        extra = Extra.forbid


@blueprint.route("/test-db-connection", methods=["GET"])
def test_db_connection():
    """Establish a connection to Postgres database"""

    host_arg = request.args.get("host")

    db_host = host_arg if host_arg else "localhost"
    db_port = 5432

    result = subprocess.run(
        f"nc -vw 0 {db_host} {db_port}",
        shell=True,
        capture_output=True,
    )

    return {
        "stdout": result.stdout.decode(),
        "stderr": result.stderr.decode(),
    }


@blueprint.route("/state-stats", methods=["GET"])
def list_state_stats():
    page = int(request.args.get("page", "0"))
    page_size = int(request.args.get("page_size", "100"))

    with get_session() as db_session:
        stats = (
            db_session.query(CovidStateStat)
            .order_by(CovidStateStat.dt, CovidStateStat.state)
            .offset(page * page_size)
            .limit(page_size)
        )

        # Maybe the user asks for a lot of data? Stream it back just in case.
        def stream():
            yield "["
            first = True
            for stat in stats:
                if not first:
                    yield ","
                yield json.dumps(stat_to_dict(stat), default=serialize_json_default)
                first = False
            yield "]"

        return Response(stream(), status=200, content_type="application/json")


@blueprint.route("/state-stats/<state>/<dt>", methods=["PATCH"])
def patch_state_stats(state, dt):
    # Could do some more validation here and return the appropriate status code if bad.
    update = request.get_json()
    update_validated = CovidStateStatUpdate(**update)

    with get_session() as db_session:
        where_clause = and_(CovidStateStat.dt == dt, CovidStateStat.state == state)
        update_payload = update_validated.dict(exclude_none=True)

        db_session.query(CovidStateStat).where(where_clause).update(update_payload)
        db_session.commit()

        stat = db_session.query(CovidStateStat).where(where_clause).first()

        if not stat:
            return "", 404

        return json.dumps(stat_to_dict(stat), default=serialize_json_default)
