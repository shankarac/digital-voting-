from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError

ROOT = Path(__file__).resolve().parents[1]


def test_alembic_upgrade_creates_enforced_schema(tmp_path, monkeypatch):
    dbfile = tmp_path / "mig.db"
    monkeypatch.setenv("DATABASE_URL", "sqlite:///" + dbfile.resolve().as_posix())
    monkeypatch.chdir(ROOT)

    cfg = Config(str(ROOT / "alembic.ini"))
    command.upgrade(cfg, "head")
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")

    engine = create_engine("sqlite:///" + dbfile.resolve().as_posix())
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    assert {"proposals", "votes", "alembic_version"} <= tables
    assert {col["name"] for col in inspector.get_columns("proposals")} == {
        "id",
        "title",
        "description",
        "created_at",
        "deadline",
        "status",
    }
    assert {col["name"] for col in inspector.get_columns("votes")} == {
        "id",
        "proposal_id",
        "voter_name",
        "vote",
        "voted_at",
    }

    with engine.begin() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")
        connection.execute(
            text(
                "INSERT INTO proposals (title, description, deadline, status) "
                "VALUES ('A', 'B', '2030-01-01 00:00:00', 'active')"
            )
        )
        connection.execute(
            text("INSERT INTO votes (proposal_id, voter_name, vote) VALUES (1, 'Amina Shah', 'yes')")
        )

    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(
                text("INSERT INTO votes (proposal_id, voter_name, vote) VALUES (1, 'Amina Shah', 'no')")
            )

    engine.dispose()
