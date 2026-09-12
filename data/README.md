# Published research data

Research cutoff: September 12, 2026.  Read Appendix A before interpreting counts.

`cfr-gaap-inventory.csv` and `usc-gaap-inventory.csv` preserve the frozen source
locators and preliminary classifications.  Rows are sentence-level observations,
not distinct legal mandates.  Deduplicate on `section_citation` for the article's
headline counts.  `names_fasb_or_asc` records whether the withheld source sentence
matched FASB, Financial Accounting Standards Board, or Accounting Standards
Codification.  Source sentences and local source-file paths are omitted.

These tables reproduce inventory arithmetic, not the underlying legal judgments.
The collection has incomplete retrievals, historical matches, and automated
classifications.  It under-covers Title 26.  Later manual statutory additions do
not constitute a complete update of the annual Code edition.  A classified
binding candidate is not a verified current compliance duty.

`codification-composition.csv` contains aggregate counts and derivation descriptions.
The underlying ASC collection is withheld.  A reader can check the paper against
the published counts but cannot independently reconstruct those counts from this
release alone.  No paragraph or glossary text is supplied.

`faf-revenue.csv` contains financial-statement facts, units, source pages, and URLs.
Despite the historical column name `amount_usd`, **use the `units` column**: many
amounts are in USD thousands.  Combined FAF/FASB/GASB observations are not FASB-only
revenue.  Licensing totals do not identify individual licensees or customer segments.
The source reports themselves are not redistributed.

`fr-mentions-by-year.csv` counts search matches, not operative legal requirements.

## Methods and verification limits

`../scripts/classify.py` preserves the sentence-level heuristic rules.  It
prioritizes qualifying incorporation clauses, GAAP self-definitions, mandatory
words, permissive words, compliance phrases, and other definitions, in that
order.  Source sentences are withheld, so the released tables cannot rerun
that classification.  The paper's Appendix A describes collection and review.

Use each table's source locators to consult the primary material.  A fresh
government response can differ from the frozen observation.  Collection tools,
raw responses, and the source archive remain outside this supplement.
`../scripts/check_public_data.py` checks the published inventory, composition,
and licensing figures against the tables; it does not validate sources or the
Federal Register search history.  `../SHA256SUMS` covers all released files.
