"""Check published aggregate arithmetic; not legal validity or source completeness."""
import csv
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(name):
    with (ROOT / "data" / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


expected = {}
for prefix in ("CFR", "USC"):
    records = rows(prefix.lower() + "-gaap-inventory.csv")
    unique = {}
    for row in records:
        key = row["section_citation"]
        if key in unique:
            assert all(unique[key][f] == row[f] for f in
                       ("title", "section_primary_mandate_type")), key
        unique[key] = row
    expected[f"n{prefix}Sections"] = len(unique)
    expected[f"n{prefix}Titles"] = len({r["title"] for r in records})
    expected[f"n{prefix}Binding"] = sum(
        r["section_primary_mandate_type"] == "binding" for r in unique.values())
    if prefix == "CFR":
        expected["nCFRAgencies"] = len({r["agency"] for r in records})
        expected["nCFRDefinition"] = sum(
            r["section_primary_mandate_type"] == "definition" for r in unique.values())
        expected["nCFRNamesFASB"] = len({r["section_citation"] for r in records
                                               if r["names_fasb_or_asc"] == "true"})
composition = {r["metric"]: r["count"] for r in rows("codification-composition.csv")}
for macro, metric in {"nTopics": "topics", "nSubtopics": "subtopics",
                      "nParagraphs": "paragraphs_total", "nSECSections": "sec_s_sections",
                      "nSECParagraphs": "sec_s_paragraphs", "nGlossaryTerms": "glossary_terms"}.items():
    expected[macro] = composition[metric]
revenue = rows("faf-revenue.csv")
for year, suffix in ((2022, "Two"), (2023, "Three"), (2024, "Four"), (2025, "Five")):
    selected = [r for r in revenue if r["fiscal_year"] == str(year)
                and r["entity"] == "FASB content"
                and r["line_item"] == "Note 2 disaggregation: licensing (FASB)"]
    assert len(selected) == 1 and selected[0]["units"] == "USD thousands"
    expected[f"licensingFASBTwenty{suffix}"] = Decimal(selected[0]["amount_usd"]) / 1000
published = {
    "nCFRSections": 785, "nCFRTitles": 39, "nCFRBinding": 472,
    "nCFRAgencies": 92, "nCFRDefinition": 70, "nCFRNamesFASB": 76,
    "nUSCSections": 83, "nUSCTitles": 16, "nUSCBinding": 73,
    "nTopics": 97, "nSubtopics": 540, "nParagraphs": 23898,
    "nSECSections": 437, "nSECParagraphs": 921, "nGlossaryTerms": 1287,
    "licensingFASBTwentyTwo": "17.903", "licensingFASBTwentyThree": "17.023",
    "licensingFASBTwentyFour": "19.191", "licensingFASBTwentyFive": "19.138",
}
assert expected.keys() == published.keys()
for name, value in expected.items():
    assert Decimal(published[name]) == Decimal(value), name
print(f"PASS: {len(expected)} published counts; no claim of legal or source validation.")
