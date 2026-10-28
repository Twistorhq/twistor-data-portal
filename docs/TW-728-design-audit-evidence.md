<!-- Prepared by Twistor Holdings LLC -->

# TW-728 Part 1 evidence: ai-design-skills implant + data portal design audit

Date: 2026-10-28. Engineer: Sofia Reyes. Branch:
`sofia/tw-728-design-audit` (twistor-data-portal, based on main
`f91340c`). Nothing merged; merge is Justynn's word only.

## The implant

- `elayadesign/ai-design-skills` (MIT, verified live from the raw
  LICENSE by Marcus) vendored at commit
  `ded7efc9d5c02761c41a03caf3b78f9259ab8828` into
  `~/workspace/custom-skills/local-twistor-landing-page-design/`:
  house-format `SKILL.md` wrapper, the upstream skill verbatim at
  `upstream/SKILL.md` (the repo's `skills/` directory holds exactly
  one skill, `landing-page-design`), upstream README, and the MIT
  `LICENSE` alongside.
- Wired into the lane: `local-twistor-design-intelligence/SKILL.md`
  now carries a "Vendored companion" section stating when Sofia
  invokes it (before builds, during builds for concrete values, at
  audit time) and the precedence order: brand board and
  design-intelligence hard gates first, vendored rules second,
  framework defaults last.

## The audit (proof of use)

Surface: data portal home page (`index.html` + `styles.css`), audited
against the vendored skill's Part A structure rules and Part B visual
rules, plus the design-intelligence `check_spec` gate and the
Impeccable detector (URL scan against a local server).

### Before (main `f91340c`)

- Impeccable: **2 anti-patterns** (line length ~91 and ~144 chars)
  and **2 advisories** (a straggler orphan word, "source." alone on a
  line; access-form placeholder contrast 3.6:1 against the 4.5:1 AA
  floor).
- `check_spec` on the portal spec: passes, 2 warnings (no palette
  selected; uncurated typefaces "Avenir Next", "Segoe UI"). The
  typeface warning converges with the vendored skill's B1 font rule.
- Vendored-skill findings with no fix applied yet: body text 17px and
  h3 at 1.2rem sit off the B1 type scale; `--radius: 10px` is not a
  B3 radius step; zero CSS transitions anywhere (B7 base curve
  absent); two button-weight CTAs above the fold (A4 pitfall);
  no favicon and no Open Graph tags (B10); no branded 404 (B10).

### Fixes applied in this branch

1. **B10 ship items:** branded `favicon.svg` (the portal's own header
   mark) linked in the head; Open Graph title, description, type,
   site name, and URL added. `og:image` is a documented gap: the repo
   holds no brand image asset to point at.
2. **B10:** new branded `404.html` in the portal's own header, hero,
   and footer pattern, `noindex`, with a way back (B10 "a way back
   from every page").
3. **B1 type scale snaps:** body 17px to 16px (text-base step);
   h3 and `.lede` 1.2rem to 1.125rem (text-lg step, snapped below
   per B1). Fluid `clamp()` headings kept as-is (responsive by
   design; documented below).
4. **B3 radius:** `--radius` 10px to 8px (rounded-lg step).
5. **B1 orphans:** `text-wrap: balance` on headings,
   `text-wrap: pretty` on paragraphs. The Impeccable straggler
   advisory is gone in the after scan.
6. **B7 motion:** transitions added on the base curve
   `cubic-bezier(0.22, 1, 0.36, 1)` at 300ms for color, background,
   and border on buttons, nav CTA, catalog chips, copy buttons, text
   links, and the catalog search input. Color-only, no layout
   properties animated. The `prefers-reduced-motion` block now also
   disables transitions.
7. **A4 hero:** the second hero CTA ("How the trust works") demoted
   from a ghost button to a text link, leaving one button-weight
   primary action above the fold ("Browse the datasets").
8. **Measure + contrast (from the Impeccable gate):** running-text
   caps at 65 to 68ch on dataset descriptions, FAQ answers, trust
   paragraphs, and page notes; access-form placeholder set to
   `#b9b2a4` at full opacity (the dark section's own secondary text
   color), clearing the 3.6:1 advisory.

### After (this branch)

- Impeccable URL scan: **0 anti-patterns, 0 advisories.** Before it
  was 2 and 2. Screenshots: `docs/tw728/portal-before.png` (main)
  and `docs/tw728/portal-after.png` (this branch), same viewport,
  captured with headless Chromium against local servers.
- `check_spec`: still passes with the same 2 warnings. They are not
  this audit's to close: picking a palette is the compose step in
  the lane workflow, and the typeface pairing is a brand decision
  (see kept findings).

### Kept on purpose, with reasons

- **B5 hero heading gradient text: NOT applied.** The vendored skill
  prescribes a gradient on hero heading text. Twistor's brand board
  and the Impeccable tells ban gradient text outright. Brand board
  wins per the lane precedence; documented conflict, not an
  oversight.
- **B1 typeface list: not applied.** The portal's "Avenir Next /
  Segoe UI" system stack is neither on the vendored skill's approved
  list nor its banned list, and `check_spec` flags it as uncurated.
  Swapping the portal's typeface is an identity call for Imani and
  Justynn, not an audit drive-by. Recommendation stands.
- **B1 "no hyphens in copy": not adopted wholesale.** It would force
  a rewrite of accurate technical copy (for example
  "provenance-stamped") across the portal for a stylistic rule that
  conflicts with Twistor's own copy standards. Noted as a divergence
  in the vendored wrapper's precedence section.
- **B2 spacing table: documented, not mass-applied.** Portal spacing
  uses many off-table values (10, 14, 20, 28px). A wholesale snap is
  a full visual rework, out of scope for an audit diff; the worst
  offenders are listed here for a future spacing pass.
- **A2 final CTA after the FAQ: not added.** The access form section
  is the conversion block and the nav CTA persists; adding a
  duplicate closing CTA section is a structural call for the next
  portal pass, recommended in this audit's notes.
- **B11 tagline reveal section: not added.** A new large-type
  section with per-word scroll activation is a feature build, not
  an audit fix. Recommended as the highest-value follow-up if
  Justynn wants the vendored skill's signature pattern on the
  portal.
- **Footer privacy and terms links (B10): not added.** No such
  pages exist and B9 bans dead links. Creating legal pages is
  Angela's lane; flagged here so it gets ticketed rather than
  faked.

## Accessibility checks

Skip link already present and kept; focus-visible outlines already
present on chips and search and kept; placeholder contrast raised
to AA on the dark form; reduced-motion now covers the new
transitions; the 404 page keeps the same semantic landmarks
(header, nav, main, footer) and a skip link.

## Honest limits

- The audit covered the home page end to end and the shared
  stylesheet. Dataset detail pages inherit the stylesheet fixes but
  were not individually audited in this pass.
- The Impeccable detector's line-length rule measures rendered
  lines in Chromium; other browsers will vary by a few characters.
