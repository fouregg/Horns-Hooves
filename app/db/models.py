import datetime
from typing import Any, Dict

from sqlalchemy import (
    Integer,
    String,
    func,
    inspect,
    Float, ForeignKey,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import current_timestamp


class Base(DeclarativeBase):
    def object_as_dict(self) -> Dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}  # noqa


class _TimestampMixin(Base):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP,
        onupdate=current_timestamp().op("AT TIME ZONE")("UTC"),
        default=datetime.datetime.utcnow,
        server_default=func.now(),
    )


class Organisation(_TimestampMixin, Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="CASCADE"),
        nullable=False
    )

    building = relationship("Building", foreign_keys=[building_id], viewonly=True)
    phones = relationship("OrganisationPhone",back_populates="organisation")
    activities: Mapped[list["Activity"]] = relationship(
        "Activity", back_populates="organisation"
    )


class OrganisationPhone(_TimestampMixin, Base):
    __tablename__ = "organisation_phones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    organisation_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False
    )

    organisation = relationship("Organisation",back_populates="phones")

class Building(_TimestampMixin, Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)


class Activity(_TimestampMixin, Base):
    __tablename__ = "activities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    parent_activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id", ondelete="CASCADE"), nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True
    )

    parent_activity = relationship("Activity", foreign_keys=[parent_activity_id], viewonly=True)
    organisation = relationship(
        "Organisation",
        back_populates="activities"
    )