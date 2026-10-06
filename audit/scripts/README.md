# Re-running this audit

Read only, five steps. All five `.js` files are Figma Plugin API code, meant to be pasted into a Claude session's `use_figma` tool call (after loading the `figma-use` skill), not run standalone. `merge.py` and `merge-components.py` are the two scripts you run yourself, on the JSON those calls produce.

File key: `vtIMgD4yMz9PjMrif2OZu0`.

## 1. Overview

Run `01-fetch-overview.js` through `use_figma`. Save the result as `../raw/00-overview.json`. This gives you every collection's id, modes and `variableIds` array, which you need for step 2.

## 2. Variables, per collection, in batches

For each collection in the overview (skip `RunTime`), copy `02-fetch-variables-batch.template.js`, fill in `COLLECTION_ID`, `COLLECTION_NAME`, `MODES` (from step 1) and a `START`/`END` slice range, run it, and save the result as `../raw/<name>_<start>-<end>.json`.

**Keep batches small enough to avoid the tool's ~20KB response cap.** As a starting point:

| Collection | Suggested batch size |
| --- | --- |
| Component Tokens, Color Mode Switch | 12–15 (long descriptions) |
| Raw Colors Values | ~18–20 (long descriptions, single mode) |
| Screen Size Switch, Semantic Tokens | ~22–25 (short/no descriptions) |
| Everything else (≤32 variables) | one batch |

If a result looks cut off, or its `variables.length` doesn't match the `START`/`END` range you asked for, **halve the batch and redo that range**: don't keep a partial result. This is exactly how 12 variables went missing the first time this audit ran (11 from Semantic Tokens, 1 from Color Mode Switch): a batch came back complete from Figma but got shortened while being saved, and it wasn't caught until `merge.py`'s alias/count checks flagged it. If you ever hit that again, re-fetch just the missing id(s) directly with `getVariableByIdAsync` (see the two `*_MISSING-*.json` files in `../raw/` for the pattern) rather than re-doing the whole batch.

## 3. Text and effect styles

Run the two calls in `03-fetch-styles.js` (one at a time: comment/uncomment as marked). Save as `../raw/text-styles.json` and `../raw/effect-styles.json`. As of the 22 Sep run-3 pass, the text style call also records `textCase`, `textDecoration`, `paragraphSpacing`, `paragraphIndent` and `leadingTrim`. Re-run this whenever a text style's case, decoration or paragraph settings might have changed, even if you're not touching variables.

## 4. Pages

For each page in the overview, copy `04-fetch-page-scan.template.js`, fill in `PAGE_ID`, and fire all pages' calls **in one parallel batch** (never loop pages inside a single call, that's the figma-use skill's page rule). Save each as `../raw/page-<name>.json`.

## 5. Components (atoms)

Only needed when a component's own structure, variants or bindings might have changed. Not every run: follow `05-fetch-components.js`: PASS 1 (one full-tree dump per component set, or per state where a set has states rather than combinable variants) to learn the shape, PASS 2 (compact bindings for every variant in one call) for the two 24-variant sets. Save results into `../raw-components/`, following the numbering merge-components.py expects (see its file list at the top of that script). Then:

```bash
python3 merge-components.py
```

Reads everything in `../raw-components/`, resolves every bound variable id against `../figma-variables.json` to a (collection, name) pair, and writes `../components.json`. Prints how many variants/states it covered (expect 65: 24 Buttons + 24 Icon-Buttons + 6 Chip + 5 Input Field states + 3 Radio states + 3 Checkbox states) and how many variable ids it could not resolve (expect 0).

**Never guess a binding from a token's name or from another variant.** The 22 Sep run 2 pilot did this for the Large button's icon gap (assumed the "Large Gap" token; Figma actually binds raw `S1`): that is exactly the mistake this step exists to prevent. Read every variant's actual bindings.

## 6. Merge and verify

```bash
python3 merge.py
```

Reads everything in `../raw/`, writes `../figma-variables.json`, and prints a verification report: counts per collection against the overview, duplicate ids, broken/unresolved aliases, and variables missing a value for one of their collection's modes. **Don't trust the output until this report is clean.** If anything's off, it tells you what to do.

After merging, re-read `../figma-variables.json` and update `../STRUCTURE.md` by hand: the report format is prose and judgement (group trees, which switches mean what, what's an anomaly), not something this script generates for you.

## Files in `../raw/` and `../raw-components/`

`../raw/`: 53 files from the original 22 Sep run 1, plus a refreshed `text-styles.json` from run 3 (adds text case/decoration/paragraph fields), are kept here as a reference for what a complete export looks like. Re-running from scratch will overwrite same-named files; delete the old ones first if you want a clean folder.

`../raw-components/`: 11 files from the run-3 component export (22 Sep 2026), covering all 65 variants/states of the six atoms. Kept as the audit trail for `../components.json`.
