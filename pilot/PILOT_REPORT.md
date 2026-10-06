# Pilot report, run 2

Read only against Figma and GitHub throughout: nothing in Figma was changed, and nothing was published anywhere.

## What was built

- **`source/figma-variables.json`**: a plain copy of `audit/figma-variables.json`.
- **`build/build.mjs`**: the full generator. It checks the export's structure, names every one of the 713 variables by the plan's rule (section 4) and verifies every name against `audit/NAME_MAP.csv`, then classifies each variable as a constant or as depending on one or more switches, and writes:
  - `dist/tokens.css`: all 713 tokens, all six switches (theme, contrast, temperature, text scale, screen size, language), following Appendix A exactly.
  - `dist/type.css`: only `Body/Default`, this run.
  - `dist/components.css`: only the primary, fill, large button, this run.
- **`build/expected.mjs`**: a separate resolver that walks `source/figma-variables.json` directly, with its own naming lookup and its own alias-walking code. It never reads `dist/tokens.css`. It writes `pilot/expected.js`, a script that sets `window.DS_EXPECTED`, so the pilot page needs no server.
- **`pilot/index.html`**: the slice, with the five switch controls, the two nested examples, the value check and the contrast check.

## What the slice is

A Background/Card surface, a paragraph in Information/Primary text using the Body/Default style, and one primary, filled, large button (fill, fill-hover, text, text-hover, border, border-hover, border width), plus every `Atoms/Buttons/Large/` token that sizes it.

## Check results

**Build.** `node build/build.mjs` and `node build/expected.mjs` both run clean.

```
[build] structure checks passed: 713 variables, all aliases resolve, all modes present,
        all 713 names verified against NAME_MAP.csv, no loops.
[build] classified 272 constants and 441 switch-dependent tokens (713 total).
[build] D1 check passed: tokens.css reads no prefers-color-scheme or prefers-contrast.
[build] wrote dist/tokens.css (90369 bytes), dist/type.css, dist/components.css

[expected] resolved 10 colour tokens x 12 combos + 13 size tokens x 18 combos = 354 values.
[expected] wrote pilot/expected.js (14568 bytes)
```

**Value check.** Opened in the in-app browser at two window widths.

| Window | Width | Automatic screen size | Result |
| --- | --- | --- | --- |
| Narrow | 400px | Mobile | All 367 values match Figma |
| Wide | 1024px | Desktop | All 367 values match Figma |

367 is 354 explicit combinations (10 colour tokens times 12 colour combinations, 13 size tokens times 18 size combinations) plus 13 more checked automatically, with no `data-screen` set anywhere, to prove the page follows the window width rather than a visitor setting (D1, D2). Both runs passed with zero differences. Colours were compared exactly; sizes and weights within 0.01; font families by their first name.

I also exercised the switch controls by hand (every one, one at a time, and in combination) and watched the visible slice change correctly, separately from the automated check.

**Contrast check.** All 48 checks pass AA, in all 12 colour combinations (12 combinations times 4 pairings: text on card at 4.5:1, button text on fill at 4.5:1 in both its default and hover states, and the focus ring on card at 3:1). The lowest ratio anywhere is 6.31:1 (button text on fill, Dark, Standard, Warm), the highest is 18.67:1 (Light or Dark, High, Cool). Every combination clears its minimum by a comfortable margin, and contrast rises with each contrast tier, as the audit predicted.

**Nesting.** Built and watched, not just checked by the script: dark, then high inside it, then warm inside that, then light inside that, four layers deep, each rendering the slice correctly at that point. Also forced mobile, then 1.4X inside it, inside an automatic desktop root. Both match what section "Appendix A" describes and what was tested in Chromium on 22 September.

## Screenshots

I looked at the slice directly in the in-app browser at all four required states, in the wide window: Light, Standard, Cool at 1X and at 2X, and Dark, High, Warm at 1X and at 2X. All four looked correct: Light, Standard, Cool showed a near-white card, dark text and a blue button; Dark, High, Warm showed a near-black card, light text and a pale green button (the High-contrast primary shade); text and button both scaled up cleanly at 2X with no colour change and no layout breakage.

**I could not save these as image files.** None of the tools in this session write a browser screenshot to a path on disk, only back to me to look at. So there are no screenshot file paths to hand you, only my own confirmation that I looked and it matched, on top of the automated value check that already covers every one of these combinations numerically. If you want image files for the record, the pilot page is a plain double-click, so a screenshot taken by hand from Arc would take a minute.

## Deviations from the plan, and why

1. **Naming rule was implemented as code, not copied from the CSV.** `build.mjs` runs the actual section 4 rule and then checks its own output against `NAME_MAP.csv`, rather than reading names from the CSV directly. This matters for the next run: when Figma adds a variable later, the build can still name it correctly on its own. Two parts of the rule were not fully spelled out in section 4 and had to be inferred, then confirmed against the CSV until all 713 matched: Raw Spacing Values drops its leading "S" before the `%50` to `_5` step (so `S%50` becomes `0_5`, not `_5`), and Lanuguage Collection takes the layer word "script". Both check out exactly against `NAME_MAP.csv`, no exceptions.
2. **The focus ring's exact CSS technique isn't specified in the plan**, only that it uses Border/Focus and has its own Focus Radius. I drew it as a box-shadow ring, and swapped the button's own corner radius to the Focus Radius token while focused, so the ring and the button share one true corner. If you had something else in mind, easy to change; nothing about the tokens themselves is affected.
3. **The language switch produces no visible branching yet.** Every language-dependent value in this file (heading font family, direction) currently resolves the same for English, Arabic and Hindi, so `tokens.css` still writes the full switch machinery for language (as one of the six), but nothing in the pilot slice exercises it, since Body/Default is fixed to Inter regardless of language. This matches what the audit already found, not a new issue.

## Anomalies I ran into but didn't act on

- `Atoms/Button/Primary/Fill/Border-Hover` resolves to the exact same Semantic Token as `Fill-Hover`, so the button's hover border is always the same colour as its hover fill. That's how Figma has it wired; the build just carries it through.
- `Atoms/Buttons/Large/Spacing/Equal` and `.../Icon Size` are in `dist/tokens.css` (all 713 are) but this pilot's button has no icon and no equal-padding state, so neither is used by `dist/components.css` yet. Expected, not a gap.

## Open questions

1. Is the focus-ring technique in section "Deviations" point 2 the one you want, or did you have a specific pattern in mind?
2. `onDark/surface/overlay` at High contrast (plan D5, the near-unreadable 1.17:1 value) doesn't touch this slice, so it didn't block anything here, but it's still waiting on your Figma edit before the full build.

## Files

- Build: [`build/build.mjs`](../build/build.mjs), [`build/expected.mjs`](../build/expected.mjs)
- Output: [`dist/tokens.css`](../dist/tokens.css), [`dist/type.css`](../dist/type.css), [`dist/components.css`](../dist/components.css)
- Pilot: [`pilot/index.html`](index.html), [`pilot/expected.js`](expected.js)
