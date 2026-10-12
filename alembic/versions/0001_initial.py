"""Create proposals and votes.

Revision ID: 0001_initial
Revises:
Create Date: 2026-10-12
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "proposals",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("deadline", sa.DateTime(), nullable=False),
        sa.Column("status", sa.Text(), server_default="active", nullable=False),
        sa.CheckConstraint(
            "status IN ('active', 'closed', 'expired')",
            name="ck_proposals_status",
        ),
        sqlite_autoincrement=True,
    )
    op.create_index("ix_proposals_status_deadline", "proposals", ["status", "deadline"])
    op.create_index("ix_proposals_created_at", "proposals", ["created_at"])

    op.create_table(
        "votes",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("proposal_id", sa.Integer(), nullable=False),
        sa.Column("voter_name", sa.Text(), nullable=False),
        sa.Column("vote", sa.Text(), nullable=False),
        sa.Column(
            "voted_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint("vote IN ('yes', 'no', 'abstain')", name="ck_votes_choice"),
        sa.ForeignKeyConstraint(["proposal_id"], ["proposals.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("proposal_id", "voter_name", name="uq_votes_proposal_voter"),
        sqlite_autoincrement=True,
    )


def downgrade() -> None:
    op.drop_table("votes")
    op.drop_index("ix_proposals_created_at", table_name="proposals")
    op.drop_index("ix_proposals_status_deadline", table_name="proposals")
    op.drop_table("proposals")
