from procurement_auditor.rules import ProcurementRuleEngine
from procurement_auditor.schemas import Evidence, RequirementItem, QuotationItem, VendorQuotation


def test_quantity_and_specification_controls():
    req = RequirementItem("Motor", {"efficiency": "IE3"}, 10, [Evidence("rfq.pdf", 2, "10 Nos IE3")])
    quote = VendorQuotation("Vendor B", items=[QuotationItem(
        "Motor", {"efficiency": "IE2"}, 12, 1450, "USD", evidence=[Evidence("quote.pdf", 3, "12 Nos IE2")]
    )])
    findings = ProcurementRuleEngine().audit([req], [quote])
    assert any(f.category == "QUANTITY" and f.severity == "CRITICAL" for f in findings)
    assert any(f.category == "SPECIFICATION" and f.severity == "CRITICAL" for f in findings)


def test_compliant_item_has_no_critical_findings():
    req = RequirementItem("Motor", {"voltage": "415V"}, 10)
    quote = VendorQuotation("Vendor A", items=[QuotationItem("Motor", {"voltage": "415V"}, 10, 1000, "USD")])
    findings = ProcurementRuleEngine().audit([req], [quote])
    assert not any(f.severity == "CRITICAL" for f in findings)
