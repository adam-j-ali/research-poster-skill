# Data integrity: reproduce the abstract before you draw it

The abstract is a claim about the data. When the author gives you the data too (a spreadsheet, an
export, an analysis workbook), recompute every number the poster will show from that data, and make
the build refuse to continue if the abstract's figures do not come out. Each rule below exists because
the plausible version was wrong on a real poster.

## 1. Treat patient-level data as confidential

- Keep it where it is. Read it in place; write only aggregates (counts, means, p-values) to the build
  folder. Never copy the spreadsheet into the project, a repo, a web tool, or a prompt to another service.
- Look at structure before values: sheet names, headers, cell types. Print values only once you know a
  sheet holds aggregates, or print counts instead of rows.
- Dates of birth, visit dates and record numbers are identifiers. A "deidentified ID" column does not make
  a sheet with dates in it deidentified.
- Some tools save large outputs to disk automatically. If one captured patient rows, redact that file and
  restrict its permissions.

## 2. Reproduce the headline numbers, and assert them

Write `analysis.py` that reads the source and computes each figure the abstract states, then `assert`s
them. Only when every assertion passes does it write `data.json`, and the poster reads only that file.

When the workbook's own summary sheet disagrees with the abstract, do not assume the abstract came from
other data. Workbooks carry live settings (a success threshold, an intention-to-treat switch) that may
have changed after the abstract was written. Recover the definition by testing the plausible variants:

- the outcome threshold (≤ vs <, 18 vs 21, and so on),
- who is in the denominator (everyone treated, only eyes/patients reaching the time point, or those plus
  earlier failures),
- whether a later rescue procedure counts as failure (it usually should).

Stop when one variant reproduces every stated figure exactly, and write that definition into the methods
panel. If none does, ask the author for the analysis file rather than guessing.

## 3. Check the statistics the abstract reports

- **SD or SE?** A mean change of whole-number counts (medications, visits) near 0.4 cannot have an SD
  below about 0.5. A tiny "± 0.18" beside a "± 1.7" is almost always a standard error mixed with an SD.
- **Paired or not?** "Decreased by 0.4" from a paired t-test should be the mean of each subject's own
  change, not the difference of two group means taken at different time points on different subjects.
  Recompute it on the same subjects; report n.
- **Which n?** The n for a paired change is the number with both measurements, often smaller than the
  cohort. Label each figure with its own n.
- **Direction and significance** should survive a correction; if a correction flips a conclusion, stop and
  tell the author.

## 4. Check the categories, not just the counts

Collaborators' workbooks often bucket free-text notes with keyword formulas. A short substring match files
unrelated notes under the wrong heading, and the label then reads as a clinical fact. Before a category
name goes on a poster:

- map each counted item back to the original note at the visit where it was recorded,
- keep the author's inclusion (which items count) and fix only the names, with a check that the totals
  are unchanged,
- read the classification formulas themselves: a device or procedure filed in the wrong group changes
  both the exclusions and what the title may claim.

## 5. Check the edges of the sheet

- The first data row may sit beside the settings block (row 2, not row 3). Compare your row count with
  the workbook's own total (its COUNT formula) and assert it.
- Duplicate header names (two "Unique ID" columns) resolve to the last one in a name-to-column map; know
  which one you are reading.

## 6. Check claims against the setting and the literature

- If the title says where or how something was done (in the office, at the bedside, by one technique),
  count how many cases actually were, and state any exceptions on the poster.
- Every comparison figure quoted from another study gets checked against that study's own abstract. A
  "69%" that the paper reports as 70% is a small error a reviewer will still find.
- When comparing with published series, say that definitions differ if they do.

## 7. Carry the loose ends to the author

Anything the data cannot settle (a truncated author list, disclosures, which numbers are final) goes into
a CONFIRMED checklist in the build. The output stays named DRAFT until every item is confirmed.
