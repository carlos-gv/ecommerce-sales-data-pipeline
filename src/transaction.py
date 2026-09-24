"""Small domain class used by the Lab1 notebook to hold and clean a single sales record."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


def _is_missing(value) -> bool:
    """True for None or NaN. pandas silently turns None into float('nan') in object columns,
    so a plain `is not None` check is not enough to detect a missing value coming from a dataframe."""
    if value is None:
        return True
    return isinstance(value, float) and value != value


@dataclass
class Transaction:
    """One e-commerce order line, plus the cleaning/derived-value logic the notebook calls."""

    order_id: str
    date: str
    customer_id: str
    product: str
    price: float
    quantity: int
    coupon_code: Optional[str]
    shipping_city: str
    discount_pct: float = field(default=0.0)

    def clean(self) -> "Transaction":
        """Normalize whitespace/casing and null out clearly invalid values. Returns self for chaining."""
        self.shipping_city = " ".join(self.shipping_city.split()).title()
        if _is_missing(self.coupon_code):
            self.coupon_code = None
        else:
            code = str(self.coupon_code).strip().upper()
            self.coupon_code = code if code else None
        if not _is_missing(self.quantity) and self.quantity <= 0:
            self.quantity = None
        if not _is_missing(self.price) and self.price <= 0:
            self.price = None
        return self

    def total(self) -> Optional[float]:
        """Revenue for this line after any percentage discount, or None if price/quantity is missing."""
        if _is_missing(self.price) or _is_missing(self.quantity):
            return None
        return round(self.price * self.quantity * (1 - self.discount_pct / 100), 2)

    def is_valid(self) -> bool:
        return not _is_missing(self.price) and not _is_missing(self.quantity) and not _is_missing(self.customer_id)

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "date": self.date,
            "customer_id": self.customer_id,
            "product": self.product,
            "price": self.price,
            "quantity": self.quantity,
            "coupon_code": self.coupon_code,
            "discount_pct": self.discount_pct,
            "shipping_city": self.shipping_city,
            "total": self.total(),
        }
