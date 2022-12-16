from typing import Optional
import sqlalchemy as sa
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


MAX_INCREMENT_VALUE = 999999999999999999999999999

# Declare the Declrative base
class Base(DeclarativeBase):
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__!s}("
            + ",".join(
                str(key) + "=" + f"{vars(self).get(key, None)!r}"
                for key in inspect(self.__class__).columns.keys()  # type: ignore[union-attr]
            )
            + ")"
        )


# Customer ORM Model of SQLAlchemy
class CustomerOrm(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        sa.Identity(start=1, cycle=True, maxvalue=MAX_INCREMENT_VALUE),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(sa.String(30), nullable=False)
    contact_number: Mapped[str] = mapped_column(sa.String(60), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Nullable Reference Required ?
    addresses: Mapped[Optional["AddressOrm"]] = relationship(back_populates="customer")

    orders: Mapped[Optional[list["OrderOrm"]]] = relationship(back_populates="customer")


# Customer Address Model of SQLAlchemy
class AddressOrm(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(
        sa.Identity(start=1, cycle=True, maxvalue=MAX_INCREMENT_VALUE),
        primary_key=True,
    )
    customer_id: Mapped[int] = mapped_column(sa.ForeignKey("customers.id"))
    present_address: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    permenent_address: Mapped[str] = mapped_column(sa.String(255))

    customer: Mapped["CustomerOrm"] = relationship(back_populates="addresses")


# As per the documentation `The association table is nearly always given as a Core Table object or
# another Core selecteable such as Join object, and is indicated by relationship.secondary argument to relationship().
# Usual, the Table uses the MetaData  object associated with the declarative base class, so that the ForeignKey directives
# can locate the remote tables with thich to link`
# refference: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationships-many-to-many

# Note: for a core table, we use the sqlalchemy.Column construct, not sqlalchemy.orm.mapped_column
product_tag_assoc_tbl = sa.Table(
    "product_tag_assoc",
    Base.metadata,
    sa.Column(
        "id",
        sa.Integer,
        sa.Identity(start=1, maxvalue=MAX_INCREMENT_VALUE, cycle=True),
        primary_key=True,
    ),
    sa.Column("product_id", sa.ForeignKey("products.id"), nullable=False),
    sa.Column("tag_id", sa.ForeignKey("tags.id"), nullable=False),
)

product_category_assoc_tbl = sa.Table(
    "product_category_assoc",
    Base.metadata,
    sa.Column(
        "id",
        sa.Integer,
        sa.Identity(start=1, maxvalue=MAX_INCREMENT_VALUE, cycle=True),
        primary_key=True,
    ),
    sa.Column("product_id", sa.ForeignKey("products.id"), nullable=False),
    sa.Column("category_id", sa.ForeignKey("categories.id"), nullable=False),
)

product_order_assoc_tbl = sa.Table(
    "product_order_assoc",
    Base.metadata,
    sa.Column(
        "id",
        sa.Integer,
        sa.Identity(start=1, maxvalue=MAX_INCREMENT_VALUE, cycle=True),
        primary_key=True,
    ),
    sa.Column("product_id", sa.ForeignKey("products.id"), nullable=False),
    sa.Column("order_id", sa.ForeignKey("orderes.id"), nullable=False),
)


class TagOrm(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(
        sa.Identity(start=1, maxvalue=MAX_INCREMENT_VALUE, cycle=True), primary_key=True
    )
    name: Mapped[str] = mapped_column(sa.String(30))

    products: Mapped[Optional[set["ProductOrm"]]] = relationship(
        secondary=product_tag_assoc_tbl, back_populates="tags"
    )


class CategoryOrm(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        sa.Identity(start=1, maxvalue=MAX_INCREMENT_VALUE, cycle=True), primary_key=True
    )
    title: Mapped[str] = mapped_column(sa.String(30), nullable=False)

    products: Mapped[Optional[set["ProductOrm"]]] = relationship(
        secondary=product_category_assoc_tbl, back_populates="categories"
    )


# Producs Model of SQLAlchemy
class ProductOrm(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        sa.Identity(start=1, maxvalue=MAX_INCREMENT_VALUE, cycle=True), primary_key=True
    )
    code: Mapped[str] = mapped_column(sa.String(30))
    name: Mapped[str] = mapped_column(sa.String(80))

    orders: Mapped[Optional[set["OrderOrm"]]] = relationship(
        secondary=product_order_assoc_tbl, back_populates="products"
    )

    tags: Mapped[Optional[set["TagOrm"]]] = relationship(
        secondary=product_tag_assoc_tbl, back_populates="products"
    )

    categories: Mapped[Optional[set["CategoryOrm"]]] = relationship(
        secondary=product_category_assoc_tbl, back_populates="products"
    )


#  Customer Order Model of SQLAlchemy
class OrderOrm(Base):
    __tablename__ = "orderes"

    id: Mapped[int] = mapped_column(
        sa.Identity(start=1, maxvalue=MAX_INCREMENT_VALUE, cycle=True), primary_key=True
    )
    invoice_no: Mapped[str] = mapped_column(sa.String(30), nullable=False)

    customer_id: Mapped["CustomerOrm"] = mapped_column(
        sa.ForeignKey("customers.id"), nullable=False
    )

    products: Mapped[set["ProductOrm"]] = relationship(
        secondary=product_order_assoc_tbl, back_populates="orders"
    )

    customer: Mapped["CustomerOrm"] = relationship(back_populates="orders")
