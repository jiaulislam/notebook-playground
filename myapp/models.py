from typing import Optional
import sqlalchemy as sa
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Declare the Declrative base
class Base(DeclarativeBase):
    pass


# Customer ORM Model of SQLAlchemy
class CustomerOrm(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        sa.Identity(start=1, cycle=True, maxvalue=999999999999999999999999999),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(sa.String(30))
    contact_number: Mapped[str] = mapped_column(sa.String(60))
    is_active: Mapped[bool] = mapped_column(default=True)

    # Nullable Reference Required ?
    addresses: Mapped[Optional["AddressOrm"]] = relationship(back_populates="customer")

    def __repr__(self) -> str:
        return (
            f"CustomerOrm("
            + ",".join(
                str(key) + "=" + f"{vars(self).get(key)!r}"
                for key in inspect(CustomerOrm).columns.keys()
            )
            + ")"
        )


# Customer Address Model of SQLAlchemy
class AddressOrm(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(
        sa.Identity(start=1, cycle=True, maxvalue=999999999999999999999999999),
        primary_key=True,
    )
    customer_id: Mapped[int] = mapped_column(sa.ForeignKey("customers.id"))
    present_address: Mapped[str] = mapped_column(sa.String(255))
    permenent_address: Mapped[str] = mapped_column(sa.String(255))

    customer: Mapped["CustomerOrm"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return (
            f"AddressOrm("
            + ",".join(
                str(key) + "=" + f"{vars(self).get(key)!r}"
                for key in inspect(AddressOrm).columns.keys()
            )
            + ")"
        )
