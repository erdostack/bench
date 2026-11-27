"""The GraphQL schema. Resolvers go straight to SQLAlchemy; there is no dataloader yet."""
import datetime as dt

import strawberry
from sqlalchemy import select

from . import models
from .db import Session


@strawberry.type
class LineItem:
    description: str
    cents: int


@strawberry.type
class Invoice:
    id: strawberry.ID
    issued_on: dt.date
    paid_on: dt.date | None
    items: list[LineItem]

    @strawberry.field
    def total_cents(self) -> int:
        return sum(i.cents for i in self.items)


@strawberry.type
class Customer:
    id: strawberry.ID
    name: str
    email: str


def _invoice(row: models.Invoice) -> Invoice:
    return Invoice(id=strawberry.ID(str(row.id)), issued_on=row.issued_on, paid_on=row.paid_on,
                   items=[LineItem(description=i.description, cents=i.cents) for i in row.items])


@strawberry.type
class Query:
    @strawberry.field
    def customers(self) -> list[Customer]:
        with Session() as s:
            return [Customer(id=strawberry.ID(str(c.id)), name=c.name, email=c.email)
                    for c in s.scalars(select(models.Customer).order_by(models.Customer.name))]

    @strawberry.field
    def unpaid_invoices(self, customer_id: strawberry.ID) -> list[Invoice]:
        with Session() as s:
            rows = s.scalars(select(models.Invoice).where(models.Invoice.customer_id == int(customer_id),
                                                          models.Invoice.paid_on.is_(None)))
            return [_invoice(r) for r in rows]


schema = strawberry.Schema(query=Query)
