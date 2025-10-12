"""Initial tables

Revision ID: 001
Revises: 
Create Date: 2025-10-12 22:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('avatar_url', sa.String(length=500), nullable=True),
        sa.Column('oauth_provider', sa.String(length=50), nullable=True),
        sa.Column('oauth_id', sa.String(length=255), nullable=True),
        sa.Column('email_verified', sa.Boolean(), nullable=True),
        sa.Column('email_verification_token', sa.String(length=255), nullable=True),
        sa.Column('password_reset_token', sa.String(length=255), nullable=True),
        sa.Column('password_reset_expires', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_oauth_id'), 'users', ['oauth_id'], unique=False)

    # Create subscriptions table
    op.create_table(
        'subscriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tier', sa.Enum('FREE', 'PRO', 'ENTERPRISE', name='subscriptiontier'), nullable=False),
        sa.Column('status', sa.Enum('ACTIVE', 'CANCELED', 'EXPIRED', 'TRIAL', name='subscriptionstatus'), nullable=False),
        sa.Column('tochka_operation_id', sa.String(length=255), nullable=True),
        sa.Column('tochka_consumer_id', sa.String(length=255), nullable=True),
        sa.Column('current_period_start', sa.DateTime(), nullable=True),
        sa.Column('current_period_end', sa.DateTime(), nullable=True),
        sa.Column('trial_start', sa.DateTime(), nullable=True),
        sa.Column('trial_end', sa.DateTime(), nullable=True),
        sa.Column('cancel_at_period_end', sa.Boolean(), nullable=True),
        sa.Column('canceled_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscriptions_tochka_operation_id'), 'subscriptions', ['tochka_operation_id'], unique=False)
    op.create_index(op.f('ix_subscriptions_user_id'), 'subscriptions', ['user_id'], unique=True)

    # Create payments table
    op.create_table(
        'payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tochka_operation_id', sa.String(length=255), nullable=False),
        sa.Column('tochka_payment_id', sa.String(length=255), nullable=True),
        sa.Column('tochka_transaction_id', sa.String(length=255), nullable=True),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('purpose', sa.String(length=500), nullable=False),
        sa.Column('status', sa.Enum('CREATED', 'PAID', 'FAILED', 'REFUNDED', 'CANCELED', name='paymentstatus'), nullable=False),
        sa.Column('payment_link', sa.String(length=500), nullable=True),
        sa.Column('payment_mode', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('subscription_tier', sa.String(length=50), nullable=False),
        sa.Column('subscription_period', sa.String(length=20), nullable=False),
        sa.Column('client_name', sa.String(length=255), nullable=True),
        sa.Column('client_email', sa.String(length=255), nullable=True),
        sa.Column('client_phone', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column('refunded_at', sa.DateTime(), nullable=True),
        sa.Column('tochka_raw_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_tochka_operation_id'), 'payments', ['tochka_operation_id'], unique=True)

    # Create app_versions table
    op.create_table(
        'app_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('version', sa.String(length=20), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('release_date', sa.DateTime(), nullable=False),
        sa.Column('changelog', sa.Text(), nullable=True),
        sa.Column('download_url', sa.String(length=500), nullable=False),
        sa.Column('file_size', sa.String(length=20), nullable=True),
        sa.Column('checksum_sha256', sa.String(length=64), nullable=True),
        sa.Column('critical', sa.Boolean(), nullable=True),
        sa.Column('min_version', sa.String(length=20), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_versions_version'), 'app_versions', ['version'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_app_versions_version'), table_name='app_versions')
    op.drop_table('app_versions')
    op.drop_index(op.f('ix_payments_tochka_operation_id'), table_name='payments')
    op.drop_table('payments')
    op.drop_index(op.f('ix_subscriptions_user_id'), table_name='subscriptions')
    op.drop_index(op.f('ix_subscriptions_tochka_operation_id'), table_name='subscriptions')
    op.drop_table('subscriptions')
    op.drop_index(op.f('ix_users_oauth_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    
    # Drop enums
    sa.Enum(name='subscriptiontier').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='subscriptionstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='paymentstatus').drop(op.get_bind(), checkfirst=True)

