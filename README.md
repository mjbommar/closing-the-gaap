# Closing the GAAP

Michael J. Bommarito II · Working paper · Research cutoff: September 12, 2026

[Read the paper (PDF)](publication/closing-the-gaap.pdf) ·
[Download the narrated body (MP3)](https://media.githubusercontent.com/media/mjbommar/closing-the-gaap/main/publication/audio/closing-the-gaap-body-charon.mp3)

The recording is a synthetic reading, approximately 2 hours 12 minutes, with
seven chapter markers.  It omits footnotes, the abstract, appendices, and
disclosures.  Consult the PDF for citations and exact wording.

## Data supplement

Five CSV tables support the paper: CFR and U.S. Code inventories, FAF revenue,
Codification composition counts, and Federal Register mentions by year.
[Data notes](data/README.md) explain fields, source locations, methods, and limits.
The classification rules are in `scripts/classify.py`.

With Python 3.11 or later, check the 19 published counts and revenue figures:

```sh
python3 scripts/check_public_data.py
sha256sum -c SHA256SUMS
```

The checker verifies arithmetic against published values.  It does not verify
the underlying legal judgments or completeness of the collection.  The source
archive, collection tools, manuscript source, and production files are maintained
separately and are not part of this public supplement.

The MP3 uses Git LFS.  If cloning, install Git LFS and run `git lfs pull` before
checking hashes.  The download link above serves the recording directly.

## Rights

The MIT license in `LICENSE` covers original software and its documentation,
not the paper, recording, or third-party quotations.  Copyright in the paper
remains with the author; this repository grants no additional license to the
paper or recording.  Readers retain rights available under applicable law.
No exclusive rights are asserted over underlying facts or government legal text.
Please cite the paper, the snapshot commit, and the identified primary sources.

The PDF includes attributed quotations for analysis.  Full third-party
publications, accounting standards, downloaded reports, commercial research,
and source sentences are not redistributed.  The tables supply factual
observations, source references, and classifications; composition is aggregate
only.  Source links confer no license to their targets.
