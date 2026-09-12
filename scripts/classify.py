"""Shared text utilities and the mandate-type classifier used by both the
CFR and USC census builders.

Classification is a simple rule-based first pass over the text of a
provision (or, where full text was not fetched, the search-excerpt text).
It is NOT a substitute for legal reading — the brief calls for "simple
rules + manual review of a sample," and the sample verification is done
separately (verify_sample.py) and recorded with verified=2026-09-11 in the
census CSVs. Mandate-type categories:

  ibr          - the provision is itself a formal incorporation-by-reference
                 clause under 1 CFR pt. 51 (only used for CFR; usually a
                 dedicated "Incorporation by reference" section, or a
                 provision whose text names 1 CFR part 51 / "incorporated by
                 reference" alongside FASB/ASC).
  definition   - defines "GAAP" (or a similarly defined term) by reference to
                 FASB and/or the Codification, without itself using
                 "shall"/"must" against a regulated party in the same
                 sentence.
  binding      - imposes a mandatory obligation ("shall"/"must"/"is required
                 to" ... "in accordance with"/"consistent with"/"comply
                 with" GAAP, or naming FASB/the ASC as the binding source),
                 including "presumed misleading if not in accordance with
                 GAAP" formulations.
  permissive   - authorizes or permits (but does not require) use of GAAP/
                 FASB standards, or references them only for interpretive/
                 cross-reference convenience.
  other        - matches a query phrase but the sentence does not fit the
                 above (e.g., statutory-construction savings clauses, index
                 entries, definitions unrelated to accounting practice).
"""
from __future__ import annotations

import re

MANDATORY_WORDS = re.compile(r"\b(shall|must|is required to|are required to|required to be)\b", re.I)
COMPLIANCE_PHRASES = re.compile(
    r"\b(in accordance with|consistent with|comply(?:ing)? with|conform(?:s|ing)? (?:to|with)|"
    r"presumed (?:to be )?misleading|not in accordance with)\b",
    re.I,
)
GAAP_TERMS = re.compile(
    r"\b(GAAP|generally accepted accounting principles|U\.S\.?\s*GAAP|"
    r"accounting principles generally accepted)\b",
    re.I,
)
FASB_TERMS = re.compile(
    r"\b(FASB|Financial Accounting Standards Board|Accounting Standards Codification|FASB ASC)\b",
    re.I,
)
DEFINE_VERBS = re.compile(
    r"\b(means|means?,|defined as|shall mean|as defined in|as set forth in|refers to|has the meaning)\b",
    re.I,
)
IBR_MARKERS = re.compile(
    r"\b(incorporat\w* by reference|1 CFR part 51|IBR approved|approved (?:by|for)"
    r" incorporation by reference|availab(?:le|ility))\b",
    re.I,
)
PERMISSIVE_WORDS = re.compile(r"\b(may|is permitted to|are permitted to|at (?:its|the) option)\b", re.I)

# A sentence that itself defines "GAAP" (or the term FASB/ASC) by reference
# to FASB/the Codification, e.g. "GAAP means ... as set forth in the
# Financial Accounting Standards Board's ... Accounting Standards
# Codification (ASC)." Distinct from a sentence that merely uses "means" to
# define some other term (e.g. "Carrying value means ... in accordance
# with GAAP"), which is an operative/binding use of GAAP, not a definition
# of GAAP itself.
GAAP_SELF_DEFINITION_RE = re.compile(
    r"^\W*(GAAP|U\.S\.?\s*GAAP|generally accepted accounting principles)\W*\s+"
    r"(means|means,|is defined as|shall mean|refers to|has the meaning)",
    re.I,
)


def classify_sentence(sentence: str, is_ibr_section: bool = False) -> str:
    """Return one of {ibr, binding, definition, permissive, other} for a
    single sentence that contains a query-phrase match."""
    s = sentence
    has_gaap = bool(GAAP_TERMS.search(s))
    has_fasb = bool(FASB_TERMS.search(s))
    if not (has_gaap or has_fasb):
        return "other"

    if is_ibr_section and IBR_MARKERS.search(s) and has_fasb:
        return "ibr"

    if GAAP_SELF_DEFINITION_RE.search(s):
        return "definition"

    modal_mandatory = bool(MANDATORY_WORDS.search(s))
    compliance_phrase = bool(COMPLIANCE_PHRASES.search(s))
    definitional = bool(DEFINE_VERBS.search(s))
    permissive = bool(PERMISSIVE_WORDS.search(s))

    # A permissive modal ("may") takes priority over a bare compliance
    # phrase like "consistent with" -- e.g. "may continue to use their
    # current accounting system ... if ... consistent with generally
    # accepted accounting principles" is permissive, not binding, even
    # though "consistent with" appears. An explicit "shall"/"must" always
    # wins regardless of any "may" elsewhere in the same sentence.
    if modal_mandatory:
        return "binding"
    if permissive:
        return "permissive"
    if compliance_phrase:
        return "binding"
    if definitional:
        return "definition"
    return "other"


SENTENCE_SPLIT_RE = re.compile(r"(?<=[.;:])\s+(?=[A-Z(§])")


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    parts = SENTENCE_SPLIT_RE.split(text)
    return [p.strip() for p in parts if p.strip()]


def find_matching_sentences(text: str, is_ibr_section: bool = False) -> list[tuple[str, str]]:
    """Return list of (sentence, mandate_type) for every sentence containing
    a GAAP/FASB/ASC term match."""
    out = []
    for sent in split_sentences(text):
        if GAAP_TERMS.search(sent) or FASB_TERMS.search(sent):
            out.append((sent, classify_sentence(sent, is_ibr_section=is_ibr_section)))
    return out
