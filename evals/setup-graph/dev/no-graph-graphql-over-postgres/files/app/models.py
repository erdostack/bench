import datetime as dt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    invoices: Mapped[list["Invoice"]] = relationship(back_populates="customer")


class Invoice(Base):
    __tablename__ = "invoice"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    issued_on: Mapped[dt.date]
    paid_on: Mapped[dt.date | None]
    customer: Mapped[Customer] = relationship(back_populates="invoices")
    items: Mapped[list["LineItem"]] = relationship(back_populates="invoice")


class LineItem(Base):
    __tablename__ = "line_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoice.id"))
    description: Mapped[str]
    cents: Mapped[int]
    invoice: Mapped[Invoice] = relationship(back_populates="items")
