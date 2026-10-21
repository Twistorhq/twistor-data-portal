# TW-667 Screenshot QA pass: Twistor Data portal (data.twistor.co)

Prepared by Twistor Holdings LLC. Run by Maya Chen, 2026-10-21, using the
local-twistor-dashboard-design skill (implanted this ticket from
abdiraimov-otabek/dashboard-design-skill, MIT). Surface chosen: the TW-604 data
portal (Twistorhq/twistor-data-portal), because it is a static HTML/CSS/JS
surface that renders and screenshots fully in this sandbox with headless
Chromium; lbt-os Trade View requires the full app stack and auth session.

Method: served the real files locally, captured before/after at 3440, 1440,
and 375 px, plus filtered and empty states, and LOOKED at every PNG. Known
totals were worked out from the detail pages independently of the index:
3 datasets; versions all v1.0; delivery all API + Excel; rows S2S-TRUST 30,
CLIMATESHIFT-1 70, CARBON-TRUST 36; catalog total 136 rows.

## Known totals check (before fixes)

- PASS: hero count 3 = 3 catalog articles = 3 detail pages.
- PASS: version v1.0 and delivery API + Excel agree on index and detail pages.
- FAIL: row counts existed only on detail pages; the catalog showed none, so
  no total could be reconciled from the catalog itself. See F1.

## Findings (ranked by harm) and fixes

- F1 HONESTY: catalog carried no row counts and no total; CLIMATESHIFT-1 reads
  "Thirty trials" on the index and "70 rows" on its detail page with the grain
  unstated, which reads as two answers to one question. FIXED: Rows (v1.0)
  added to every catalog meta panel (30 / 70 / 36, matching the detail tables
  exactly); a stated count line under the catalog controls reports the shown
  count and the catalog total, and the total is computed in app.js from the
  rendered Rows values so it cannot drift from the panels.
- F2 HONESTY: the synthetic-seed disclosure sat in one note after all three
  datasets; at 375 px the first dataset reads as real data for a long scroll.
  FIXED: a "Synthetic seed" chip on every dataset row, visible at all widths;
  the original honest note stays.
- F3 HONESTY: pricing cards held no figures at all ("Toll-metered", "One-time
  fee"), against the standing Twistor toll rule. FIXED: cards now state
  "$0.01 to $0.10 per call" and "$0.01 to $0.10 per download", and the pricing
  note states the $0.10 ceiling and that the exact fee is shown before payment.
- F4 LAYOUT: the flipped (alternating) CLIMATESHIFT-1 row kept the base grid
  columns, so its prose was squeezed into the 280 px column and its meta panel
  stretched across the wide column; obvious at 3440 and 1440. FIXED: the flip
  variant swaps the grid columns (280 px + 1 fr).
- F5 LAYOUT: at 3440 px the 1080 px content column floated between wide empty
  bands, the upstream ultrawide smell. FIXED: wide mode at 112.5 rem and up
  grows the wrap to 1480 px (narrow text wraps keep their measure); the
  after-3440 screenshot shows the content column about 40 percent wider.
- F6 COMPONENT: the catalog had no filter, no result count, and no empty
  state. FIXED: domain chips (selected = soft tinted fill + ring, per the
  skill), a search input, an aria-live result count, and a structured empty
  state with a clear action. Filter and search state also read from ?lane=
  and ?q= so any state is shareable and screenshot-able. Evidence:
  after-filter-carbon-1440.png ("Showing 1 of 3") and after-empty-1440.png
  ("Showing 0 of 3" + empty panel).
- F7 POLISH: numbers were not tabular, and the detail-page version tables
  left-aligned the numeric Rows column as text. FIXED: tabular figures on KPI
  values, meta values, and table cells; Rows column right-aligned. Evidence:
  after-detail-carbon-1440.png (36, right-aligned, matches the index panel).
- F8 REGRESSION CAUGHT BY THIS PASS (round 2): the first after-375 screenshot
  showed the flipped row's meta panel clipped off the right edge of the phone
  viewport, because the flipped-row column rule out-specified the small-screen
  single-column rule. FIXED with an explicit flipped-row rule inside the
  860 px media query and re-captured; after-375.png is clean, chips wrap, no
  sideways scroll, no clipped panels.
- F9 OBSERVATION, DEFERRED (not a design fix): the hero KPI "100% of rows
  carry a method code" generalises a property the detail pages document most
  concretely for CARBON-TRUST (method codes), while S2S-TRUST documents truth
  lineage and CLIMATESHIFT-1 management coding. Whether 100 percent holds per
  dataset is a data claim for the data owner (Dre) to confirm; copy unchanged.

## Screenshots (this folder)

- before-1440.png, before-375.png, before-3440.png: pre-fix surface.
- after-1440.png, after-375.png, after-3440.png: post-fix, same widths.
- after-filter-carbon-1440.png: lane filter applied, 1 of 3 shown.
- after-empty-1440.png: search with no match, structured empty state.
- after-detail-carbon-1440.png: detail-page table alignment check.

Branch only (maya/tw-667-dashboard-design). Nothing merged; Rosa reviews,
Justynn gives the merge word.
