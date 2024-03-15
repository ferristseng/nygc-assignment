from api import create_app
from api.db import init_db
from dotenv import load_dotenv


if __name__ == "__main__":
    app = create_app()

    # Need the env vars to initialize the SQLALchemy engine
    load_dotenv(".env")

    init_db()

    app.run(
        host="0.0.0.0",
        load_dotenv=True,
        port=5001
    )
