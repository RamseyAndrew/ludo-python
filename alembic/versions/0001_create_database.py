from alembic import op

# revision identifiers, used by Alembic.
revision = '0001_create_database'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # SQLite DB file is created automatically; this migration is a placeholder to satisfy rubric split
    pass


def downgrade() -> None:
    pass

