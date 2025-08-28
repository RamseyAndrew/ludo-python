from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_create_tables'
down_revision = '0001_create_database'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'players',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('color', sa.String(20), nullable=False),
    )

    op.create_table(
        'games',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('started_at', sa.DateTime, nullable=False),
        sa.Column('ended_at', sa.DateTime, nullable=True),
        sa.Column('winner_player_id', sa.Integer, sa.ForeignKey('players.id'), nullable=True),
    )

    op.create_table(
        'game_players',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('game_id', sa.Integer, sa.ForeignKey('games.id'), nullable=False),
        sa.Column('player_id', sa.Integer, sa.ForeignKey('players.id'), nullable=False),
    )

    op.create_table(
        'moves',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('game_id', sa.Integer, sa.ForeignKey('games.id'), nullable=False),
        sa.Column('player_id', sa.Integer, sa.ForeignKey('players.id'), nullable=False),
        sa.Column('turn_index', sa.Integer, nullable=False),
        sa.Column('dice', sa.Integer, nullable=False),
        sa.Column('token_index', sa.Integer, nullable=False),
        sa.Column('old_pos', sa.Integer, nullable=False),
        sa.Column('new_pos', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('moves')
    op.drop_table('game_players')
    op.drop_table('games')
    op.drop_table('players')

