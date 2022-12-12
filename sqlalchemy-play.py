# %%
from typing import Optional
import sqlalchemy as sa
from sqlalchemy.inspection import inspect
from devtools import debug
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from pydantic import BaseModel, Field, NoneStr
from datetime import datetime
from faker import Faker

# %%
engine = sa.create_engine("oracle+cx_oracle://jibon:sys123@LOCAL", echo=True)

# %% [markdown]
# ### DECLARATIVE BASE STYLE 2.0
#

# %%
class Base(DeclarativeBase):
    pass


# %%
metadata_obj = sa.MetaData()

# %%
class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(30))
    age: Mapped[int] = mapped_column(nullable=True)
    salary: Mapped[str] = mapped_column(sa.String(30))
    address: Mapped[str] = mapped_column(sa.String(80))

    def __repr__(self) -> str:
        return f"Customer(id={self.id!r}, name={self.name!r}, salary={self.salary!r})"


# %% [markdown]
# #### Reflection Of Existing Table
#

# %%
tbl_order = sa.Table(
    "demo_orders",
    metadata_obj,
    sa.Column("order_id", sa.Integer, primary_key=True, key="id"),
    sa.Column("customer_id", sa.Integer, sa.ForeignKey(Customer.id)),
    autoload_with=engine,
)

# %% [markdown]
# #### Declarative Class of Existing Reflected Tables
#

# %%
class Order(Base):
    __table__ = tbl_order
    # customer_id: Mapped[int] = mapped_column(sa.ForeignKey('customers.id'))
    def __repr__(self) -> str:
        return "<Order({!r})".format(vars(self))
        # return f"Order(id={self.id!r}, user_name={self.user_name!r}, timestamp={self.order_timestamp!r})"


# %% [markdown]
# ### FAKER DATA
#

# %%
fake = Faker()

# %%
class CustomerSchema(BaseModel):
    id: int
    name: NoneStr = None
    age: Optional[int] = None
    address: NoneStr = None
    salary: float


# %%
class OrderSchema(BaseModel):
    customer_id: int
    order_total: float
    order_timestamp: Optional[datetime] = None
    user_name: NoneStr = None
    tags: NoneStr = None

    class Config:
        allow_population_by_field_name = True


# %%
def generate_fake_customer(id: int) -> Customer:
    _customer = CustomerSchema(
        id=id,
        name=fake.name(),
        age=fake.random_int(min=18, max=100),
        address=fake.address(),
        salary=fake.random_int(min=10000, max=1000000),
    )
    return Customer(**_customer.dict())


def generate_fake_order(customer_id: int) -> Order:
    _date = fake.date_between(start_date="today", end_date="+1y")
    _order = OrderSchema(
        customer_id=customer_id,
        order_total=fake.random_int(min=100, max=55000),
        order_timestamp=datetime(_date.year, _date.month, _date.day),
        user_name=fake.name(),
        tags=fake.lexify(text="??????????"),
    )
    return Order(**_order.dict())


# %%
## GENERATE DUMMY DATA
# customers = [generate_fake_customer(i) for i in range(1001, 20000)]

# %% [markdown]
# #### ADDING FAKE DATA TO TABLE
#

# %%
# with sa.orm.Session(bind=engine) as session:
#     session.add_all(customers)
#     session.commit()

# %%
# with sa.orm.Session(bind=engine) as session:
#     stmt = sa.select(Customer).order_by(sa.desc(Customer.id))

#     for customer in session.scalars(stmt).all():
#         # debug(key, customer)
#         session.add(generate_fake_order(customer.id))

#     session.commit()
# customers = session.execute(stmt).scalars().all()

# for key, customer in enumerate(customers):
#     debug(generate_fake_order(key, customer.id))


# %%
# Normal Selecct
with Session(bind=engine) as session:
    stmt = sa.select(Order).limit(10)
    _customers = session.execute(stmt).scalars().first()
    debug(_customers)

# %%
class CustomerOrder(BaseModel):
    order_id: int = Field(alias="id")
    order_amount: float = Field(alias="order_total")
    order_date: datetime = Field(alias="order_timestamp")
    name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# %%
# Join Select

with Session(bind=engine) as session:
    stmt = (
        sa.select(
            tbl_order.columns.id,
            tbl_order.columns.order_total,
            tbl_order.columns.order_timestamp,
            Customer.name,
        )
        .join_from(tbl_order, Customer)
        .where(tbl_order.columns.customer_id == 20)
        .order_by(sa.desc(tbl_order.columns.id))
        .limit(10)
    )
    _customer_orders: list[CustomerOrder] = [
        CustomerOrder(**record._asdict()) for record in session.execute(stmt).all()
    ]

    debug(_customer_orders)

# %%
db = Session(bind=engine)

query = db.query(Order)


# response_range = "{}/{}".format(Order.__name__.lower(), count)
# %%
filter_params = ["user_name:roberts"]

conditions = []

for filter in filter_params:
    for key, *params in [filter.split(":", 1)]:
        if len(params):
            debug(params)
            if key in inspect(Order).columns.keys():
                conditions.append(
                    sa.cast(Order.__dict__[key], sa.String).ilike("%" + params[0] + "%")
                )
            query = query.filter(sa.or_(*conditions))


result = query.all()

debug(result)
# %%
