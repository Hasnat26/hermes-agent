from dataclasses import dataclass, asdict
from typing import Any

from .schemas import RequirementItem, VendorQuotation


@dataclass
class Finding:
    severity: str
    category: str
    vendor: str
    item: str
    message: str
    evidence: list[dict[str, Any]]

    def as_dict(self):
        return asdict(self)


class ProcurementRuleEngine:
    """Deterministic controls. No LLM is used to calculate decisions."""

    def __init__(self, quantity_tolerance_pct: float = 0.0):
        self.quantity_tolerance_pct = quantity_tolerance_pct

    @staticmethod
    def _norm(value):
        return str(value).strip().lower().replace(" ", "") if value is not None else None

    def audit(self, requirements: list[RequirementItem], quotations: list[VendorQuotation]):
        findings: list[Finding] = []
        req_by_name = {self._norm(x.item): x for x in requirements}

        for q in quotations:
            for item in q.items:
                req = req_by_name.get(self._norm(item.item))
                if req is None:
                    findings.append(Finding("WARNING", "TECHNICAL", q.vendor, item.item,
                                            "Quoted item is not present in the requirement baseline.",
                                            [asdict(e) for e in item.evidence]))
                    continue

                if req.quantity is not None and item.quantity is not None:
                    variance_pct = ((item.quantity - req.quantity) / req.quantity * 100) if req.quantity else 0
                    if abs(variance_pct) > self.quantity_tolerance_pct:
                        severity = "CRITICAL"
                        findings.append(Finding(
                            severity, "QUANTITY", q.vendor, item.item,
                            f"Required quantity={req.quantity}; quoted quantity={item.quantity}; variance={variance_pct:+.2f}%.",
                            [asdict(e) for e in item.evidence] + [asdict(e) for e in req.evidence],
                        ))

                for key, required_value in req.specification.items():
                    quoted_value = item.specification.get(key)
                    if quoted_value is None:
                        findings.append(Finding(
                            "WARNING", "SPECIFICATION", q.vendor, item.item,
                            f"Required specification '{key}' is missing from the quotation.",
                            [asdict(e) for e in item.evidence] + [asdict(e) for e in req.evidence],
                        ))
                    elif self._norm(quoted_value) != self._norm(required_value):
                        findings.append(Finding(
                            "CRITICAL", "SPECIFICATION", q.vendor, item.item,
                            f"Specification mismatch for {key}: required='{required_value}', quoted='{quoted_value}'.",
                            [asdict(e) for e in item.evidence] + [asdict(e) for e in req.evidence],
                        ))

        # Commercial comparison is descriptive; it does not declare a vendor winner.
        for item_name in {i.item for q in quotations for i in q.items}:
            priced = [i for q in quotations for i in q.items if self._norm(i.item) == self._norm(item_name) and i.unit_price is not None]
            if len(priced) > 1:
                prices = [i.unit_price for i in priced]
                low, high = min(prices), max(prices)
                if low and (high - low) / low > 0.10:
                    findings.append(Finding(
                        "WARNING", "COMMERCIAL", "MULTI-VENDOR", item_name,
                        f"Unit-price spread is {(high-low)/low*100:.2f}% across quotations.",
                        [asdict(e) for i in priced for e in i.evidence],
                    ))
        return findings
