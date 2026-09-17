import argparse
import json
from pathlib import Path

from .report import markdown_report
from .rules import ProcurementRuleEngine
from .schemas import Evidence, RequirementItem, QuotationItem, VendorQuotation


def load_requirements(path):
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [RequirementItem(**x, evidence=[Evidence(**e) for e in x.get("evidence", [])]) for x in raw]


def load_quotations(path):
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    result = []
    for q in raw:
        items = []
        for x in q.get("items", []):
            items.append(QuotationItem(**x, evidence=[Evidence(**e) for e in x.get("evidence", [])]))
        result.append(VendorQuotation(vendor=q["vendor"], reference=q.get("reference", ""), items=items,
                                      tax=q.get("tax"), freight=q.get("freight"), payment_terms=q.get("payment_terms", ""),
                                      evidence=[Evidence(**e) for e in q.get("evidence", [])]))
    return result


def main():
    parser = argparse.ArgumentParser(description="Local Procurement Auditor")
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit")
    audit.add_argument("requirements")
    audit.add_argument("quotations")
    audit.add_argument("--out", default="procurement_audit.md")
    args = parser.parse_args()

    requirements = load_requirements(args.requirements)
    quotations = load_quotations(args.quotations)
    findings = ProcurementRuleEngine().audit(requirements, quotations)
    report = markdown_report(requirements, quotations, findings)
    Path(args.out).write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
