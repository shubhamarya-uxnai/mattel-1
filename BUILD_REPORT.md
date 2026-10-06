# Build report, run 3 (the full build)

Read only throughout: nothing in Figma was changed, and nothing was published to GitHub.

## What was built

**The export**, completed:
- Text styles re-exported with case, decoration and paragraph settings (`audit/scripts/03-fetch-styles.js`, extended). Confirms the plan's prediction exactly: Table/Column-Header, Label/Caption and Label/Micro are UPPER; Link/Default is UNDERLINE; no paragraph spacing, indent or leading trim anywhere.
- The six atom component sets exported in full: every variant's own bindings, by collection and name, read from Figma directly (`audit/scripts/05-fetch-components.js`, new; `audit/components.json`, 182KB, all 65 variants and states, 0 unresolved bindings).

**The build**, extended (`build/build.mjs`; `dist/tokens.css` untouched, still exactly the file the pilot proved):
- `dist/type.css`: all 16 type styles now, not just Body/Default.
- `dist/components.css`: the six atoms, generated from `audit/components.json`'s real bindings.
- `dist/shadcn.css`, `dist/tailwind.css`, `dist/fonts.css`, `dist/tokens.json`: new this run.
- `build/expected.mjs`: extended to resolve every offered token, every atom's bindings, and the 67 contrast pairs, independently of the CSS.

**The specimen** (`specimen/index.html`, new): switch controls for all six switches, the type section next to Figma's own sample text, all 127 component colours and 117 responsive numbers, all 65 atom variants and states working live, a shadcn-only card, the pilot's nested examples, and three checks.

## Check results

```
node build/build.mjs
  structure checks passed: 713 variables, all aliases resolve, all modes present,
  all 713 names verified against NAME_MAP.csv, no loops.
  classified 272 constants and 441 switch-dependent tokens (713 total).
  D1 check passed: tokens.css reads no prefers-color-scheme or prefers-contrast.

node build/expected.mjs
  colour: 127 component + 37 shadcn tokens x 12 combos
  size: 117 responsive numbers + 3 family tokens x 18 combos
  component checks: 191
  contrast pairs: 67
```

At `specimen/index.html`, in both a narrow window (400px, resolves to Mobile) and a wide one (1200px, resolves to Desktop):

| Check | Result |
| --- | --- |
| Value | **All 4,248 values match Figma.** (127 colours + 37 shadcn names, 12 combinations each; 117 sizes + 3 font-family tokens, 18 combinations each; plus 120 more checked with no `data-screen` set at all, to prove the automatic switch, not a guess) |
| Component | **All 730 component properties read the token Figma binds.** Every variant of Buttons and Icon-Buttons, in its own colours and again in Dark; every Chip variant; all five Input Field states; all three Radio and three Checkbox states. |
| Contrast | **802 of 804 checked pairs pass AA**, in all 12 colour combinations. The 2 that fail are the known one: `Information/Primary` on `Layer/Layer 3`, Dark, High, both Cool and Warm, 1.17:1 (D5, still waiting on the Figma edit). No other pairing fails anywhere. |

Both windows gave identical results; the two runs above are the same numbers checked twice, once each way.

## How the atoms compare with Figma

**Type.** Compared side by side against the Figma specimen frame directly (`get_screenshot` of node `73:641`): same eight groups, same order, same sample text, same weight and case treatment on every one of the 16 styles. No difference.

**Buttons.** Compared against the Figma component set (`get_screenshot` of node `21:86`): the 6-row-by-4-column grid there is Type and Size down the rows, Fill and Hover across the columns, exactly the grouping `dist/components.css` generates the colours and layout by. Same blue for Primary, same teal for Secondary, same grey for Neutral, same pattern of filled versus outlined for Fill On/Off. No difference.

**The other five atoms** (Icon-Buttons, Chip, Input Field, Radio Button, Checkbox) were not separately screenshotted against Figma. Every one of their properties, in every variant and state, already passed the exact numeric component check above, which is a stronger proof than a side-by-side look would add: it does not just look the same, it reads the same token Figma binds, to four-decimal precision on sizes and exact hex on colours.

## The Gradient Creator result

The Framer component (`framer/GradientCreator.tsx`) cannot be opened outside Framer itself, so this was tried a different way that proves the same thing: its own loader code was read to find exactly what it does (append the design system's `<link>` tags after the studio's own, then add a `dark` class to the root), and that was done directly against the running studio, live, in a browser.

Before, the studio's own theme:

```
--background: #0a0b0f   --card: #111219   --primary: #7d8cff
--border: #242838       --ring: #7d8cff   --radius: 9px
```

After adding `tokens.css` and `shadcn.css` from this build and setting dark mode, with nothing else touched:

```
--background: #080c17   --card: #191d2c   --primary: #70a3d9
--border: #4f5d72       --ring: #70a3d9   --radius: 12px
--font-sans: "Inter", ui-sans-serif, system-ui, sans-serif
```

Every one of those six matches this system's Dark, Standard, Cool values exactly (checked against the same numbers the specimen already proved). The background shifts to a cooler, bluer dark; the accent colour moves from periwinkle to this system's own blue; borders and the corner radius follow. The visible change in the settings panel itself is subtle, since most of its controls are native sliders that do not read these names, but the six variables that ARE meant to restyle it did, with no Gradient Creator file touched.

## Deviations from the plan, and why

1. **The focus ring is drawn with an `outline`, with its corner radius swapped in only while focused** (plan D9). A CSS outline has no radius property of its own; it always follows the element's current `border-radius`. This is the only way to satisfy D9's own check ("its corners equal Focus Radius") while still using a real outline, never a shadow. `outline-offset` is `calc(4px - width)` rather than a fixed `3px`, so the ring's outer edge always lands exactly 4px out (Figma's own literal, unbound number) whatever the width token happens to be.
2. **Two numbers in Figma's own button and radio geometry are not bound to any token, so the code does not invent one either:** the focus ring's 4px offset and 8px size delta (both button sizes, identical), and the radio's inner dot (10px) and checkbox's indeterminate dash (7×1px). These are written as plain literals, matching exactly what Figma itself does.
3. **Radio Button's third "State", Selected Tick, is offered as a style modifier (`data-mark="tick"`), not a fourth interaction state.** A native `<input type="radio">` only has checked and unchecked; Figma's own three-way State property does not map onto that directly. Selected Tick still uses `:checked`, with an extra attribute choosing which of the two selected looks (a plain dot, or a solid fill with a checkmark) to show.
4. **Icons are Phosphor SVGs (MIT licensed), imported directly, not recreations of Figma's own icon vectors** (`bx-refresh`, `bx-user`, and so on). Those layers are Figma `INSTANCE_SWAP` properties, placeholders meant to be swapped for whatever icon a real usage needs; only their size and colour are tokens. Six were fetched (`user`, `calendar`, `question`, `check`, `arrow-clockwise`, `arrow-right`) to cover every icon slot the specimen shows.
5. **Two known Figma-authoring quirks are carried through exactly as bound, not corrected:** the Input Field's Error state background reads the same `Atoms/Input Field/Disabled` token the Disabled state uses, not a separate error background; and the Radio/Checkbox tick mark and Chip's icon share one `Atoms/Chip/Spacing/Icon Size` token rather than each having its own. Both are visible in `audit/components.json`; neither is a code decision.
6. **`dist/tailwind.css` has not been run through an actual Tailwind build.** No installs, per the ground rules, so there is no way to compile it here. Written to Tailwind v4's CSS-first syntax (`@theme inline`, `@custom-variant`, `@utility`) to the best of available knowledge; check it compiles before relying on it.
7. **`dist/tokens.json` uses flat top-level keys** (one per code name, e.g. `--ds-color-button-primary-fill-fill`) rather than a nested group tree, since the code names are already fully qualified and globally unique. A tool expecting deep nesting may need a light re-shape.

## Open questions

1. **D5, the overlay/Layer-3 value, is still outstanding.** Once `onDark/surface/overlay` High is fixed in Figma (probably to `base/850`, per the audit) and re-exported, the contrast check should read 804 of 804, with nothing to mark as known.
2. **The focus-ring technique** (outline, radius swapped in on focus, calc-based offset) is a specific reading of D9; if a different implementation was intended, it's a small, contained change (one function in `build.mjs` per component).
3. **Should `--radius` and `--font-sans` (the two shadcn names that are not colours) get their own line in a future check pass?** Right now they're proven correct indirectly, since they alias tokens the value check already covers directly; this run treated that as sufficient rather than adding two more numbers to track.
4. **D6, D7 (dashboard patterns), D8 (writing names back to Figma)** all still stand as before; nothing here changes them.

## Files

- Export: [`audit/components.json`](audit/components.json), [`audit/scripts/05-fetch-components.js`](audit/scripts/05-fetch-components.js), [`audit/scripts/merge-components.py`](audit/scripts/merge-components.py)
- Build: [`build/build.mjs`](build/build.mjs), [`build/expected.mjs`](build/expected.mjs)
- Output: everything in [`dist/`](dist/)
- Specimen: [`specimen/index.html`](specimen/index.html)
- Usage: [`README.md`](README.md)
