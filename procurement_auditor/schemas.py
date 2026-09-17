from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Evidence:
    document: str
    page: Optional[int] = None
    quote: str = ""


@dataclass
class RequirementItem:
    item: str
    specification: dict[str, str] = field(default_factory=dict)
    quantity: Optional[float] = None
    evidence: list[Evidence] = field(default_factory=list)


@dataclass
class QuotationItem:
    item: str
    specification: dict[str, str] = field(default_factory=dict)
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    currency: Optional[str] = None
    delivery_days: Optional[int] = None
    warranty_months: Optional[int] = None
    evidence: list[Evidence] = field(default_factory=list)


@dataclass
class VendorQuotation:
    vendor: str
    reference: str = ""
    items: list[QuotationItem] = field(default_factory=list)
    tax: Optional[float] = None
    freight: Optional[float] = None
    payment_terms: str = ""
    evidence: list[Evidence] = field(default_factory=list)
