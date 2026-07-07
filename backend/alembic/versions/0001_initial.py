from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
def upgrade():
    op.create_table('medicines',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('generic_name', sa.String(length=255), nullable=False),
        sa.Column('brand_name', sa.String(length=255), nullable=True),
        sa.Column('atc_code', sa.String(length=50), nullable=True),
        sa.Column('dosage_form', sa.String(length=100), nullable=True),
        sa.Column('strength', sa.String(length=100), nullable=True),
        sa.Column('who_essential', sa.Boolean(), nullable=True),
        sa.Column('country_code', sa.CHAR(length=2), nullable=True, server_default='IQ'),
        sa.Column('local_production_status', sa.String(length=50), nullable=True, server_default='none'),
        sa.Column('annual_import_estimate_usd', sa.Numeric(), nullable=True),
        sa.Column('data_confidence', sa.String(length=50), nullable=True, server_default='seed'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table('active_ingredients',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('manufacturing_complexity', sa.String(length=20), nullable=True),
        sa.Column('patent_status', sa.String(length=20), nullable=True),
        sa.Column('patent_expiry_date', sa.Date(), nullable=True),
    )

    op.create_table('manufacturers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('country_code', sa.CHAR(length=2), nullable=True),
        sa.Column('is_local', sa.Boolean(), nullable=True),
        sa.Column('gmp_certified', sa.Boolean(), nullable=True),
    )

    op.create_table('factories',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('manufacturer_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('governorate', sa.String(length=100), nullable=True),
        sa.Column('gmp_status', sa.String(length=50), nullable=True),
        sa.Column('capacity_units_per_year', sa.Numeric(), nullable=True),
    )

    op.create_table('imports',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('medicine_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('source_country_code', sa.CHAR(length=2), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('volume_units', sa.Numeric(), nullable=True),
        sa.Column('cost_usd', sa.Numeric(), nullable=True),
    )

    op.create_table('pli_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('medicine_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('score', sa.Numeric(5,2), nullable=False),
        sa.Column('factor_breakdown', postgresql.JSONB(), nullable=True),
        sa.Column('computed_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('model_version', sa.String(length=50), nullable=True),
    )

    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=True),
        sa.Column('oauth_provider', sa.String(length=50), nullable=True),
        sa.Column('role', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table('audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(length=255), nullable=True),
        sa.Column('entity_type', sa.String(length=100), nullable=True),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('diff', postgresql.JSONB(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('users')
    op.drop_table('pli_scores')
    op.drop_table('imports')
    op.drop_table('factories')
    op.drop_table('manufacturers')
    op.drop_table('active_ingredients')
    op.drop_table('medicines')
