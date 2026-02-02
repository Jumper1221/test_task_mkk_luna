import sys
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


if "alembic" in sys.modules:
    from app.models.activities import Activity  # noqa: F401
    from app.models.buildings import Building  # noqa: F401
    from app.models.organization_activities import OrganizationActivity  # noqa: F401
    from app.models.organizations import Organization  # noqa: F401
    from app.models.phones import Phone  # noqa: F401
