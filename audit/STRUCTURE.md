# TEST NEW — Variables structure

File key `vtIMgD4yMz9PjMrif2OZu0`. Inspected 2026-09-22, read only, via the Figma plugin API (not the community-plugin fallback). The collection named `RunTime` was ignored throughout, as instructed (it holds one variable). All other counts, aliases and modes below come from a full export of the ten in-scope collections, cross-checked by script against the Variables panel counts, against every alias target, and against every mode of every variable.

Companion file: `figma-variables.json`, same folder.

## 1. Collections

| Collection | Variables | Modes | Default | What the modes appear to be |
| --- | --- | --- | --- | --- |
| Typography Useable Tokens | 32 | Mode 1 | Mode 1 | single mode, no switching: just a naming layer over font family, sizes and weights |
| Component Tokens | 141 | Light, Dark | Light | light and dark colour appearance |
| Screen Size Switch | 130 | Mobile, Tablet, Desktop | Mobile | breakpoint: responsive spacing and type scale. Tablet and Desktop are identical in every one of the 130 variables, with zero exceptions, so this behaves as a two-value switch (Mobile vs. everything else) dressed as three |
| Raw Spacing Values | 23 | Mode 1 | Mode 1 | single mode: a plain spacing scale |
| Color Mode Switch | 90 | Cool, Warm | Cool | colour temperature: a second palette axis, independent of light/dark |
| Raw Colors Values | 130 | Value | Value | single mode: raw colour ramps |
| Lanuguage Collection | 2 | Mode 1 | Mode 1 | single mode: font metadata for one script system, named "Roman" (typo in the collection name: "Lanuguage") |
| Language Switch | 2 | English, Arabic, Hindi | English | script/writing system. All three modes currently resolve to the same "Roman" values, so no script other than Roman has been built out yet |
| Raw Font Size Values | 21 | 1X, 1.2X, 1.4X, 1.6X, 1.8X, 2X | 1X | text-scale accessibility multiplier. Confirmed exact: every size at every mode is the 1X value times 1.0/1.2/1.4/1.6/1.8/2.0 |
| Semantic Tokens | 142 | Standard, Medium, High | Standard | contrast tier: a WCAG-style accessibility contrast boost |

RunTime (1 variable, out of scope) was not exported.

## 2. Layers

Reading from raw values up to what actually gets bound to layers:

```
Raw Colors Values (130)
        |  90 aliases
        v
Color Mode Switch (90)
        |  142 aliases
        v
Semantic Tokens (142) ------------------------.
        |  127 aliases (all 127 COLOR vars;    |
        |  the other 14 Component Tokens are   |
        |  literal border-width floats, 0 or 1)|
        v                                       |
Component Tokens (141) <----------------------'

Raw Spacing Values (23)
        |  66 aliases
        v
Screen Size Switch (130) <---- also aliases 49 vars from
        ^                       Typography Useable Tokens
        |
Raw Font Size Values (21)
        |  21 aliases
        v
Typography Useable Tokens (32)
        ^
        |  1 alias (Font Family/Primary only)
Language Switch (2)
        |  2 aliases
        v
Lanuguage Collection (2)
```

Every alias in the file resolves to a variable that exists (0 broken, checked against all 713). Component Tokens and Semantic Tokens are pure alias layers: not one of their colour variables carries a raw hex value, every single one points down the chain. That is a clean, disciplined build.

## 3. Switches

Four independent switches exist, held in four different collections, plus one pair of ideas that is split across two different mechanisms:

- **Light / Dark** — lives as the two modes of **Component Tokens** (Light, Dark). It is also written a second way, as **`onLight/…` and `onDark/…` name prefixes inside Semantic Tokens** rather than as a mode. Semantic Tokens has one mode axis already (Standard/Medium/High, the contrast tier) and can't carry a second one on top of it in Figma, so light/dark had to become a naming split instead of a mode split. Every `onLight/x` has a matching `onDark/x`: I checked all twelve subgroups (surface, layer, on-fill, border, action/primary, action/secondary, action/neutral, chart, status/error, status/warning, status/success, status/info) and each pairs 1:1, 71 onLight to 71 onDark, no orphans.
- **Cool / Warm** — the two modes of **Color Mode Switch**. Of its 90 tokens, 50 resolve to the identical raw colour in both modes and 40 differ. The ones that differ are the brand-adjacent families (primary, secondary, tertiary) and the neutral "base" ladder; the ones that stay identical are error, warning, success and informative, which apparently don't get a warm retint.
- **Screen size** — the three modes of **Screen Size Switch** (Mobile, Tablet, Desktop), described above. Worth restating: Tablet and Desktop have never once diverged across 130 tokens.
- **Contrast tier** — the three modes of **Semantic Tokens** (Standard, Medium, High). This is why the "base" neutral ramp in Color Mode Switch has 20 steps (0, 50, 100, 150, 200 … 950) while every other ramp (primary, secondary, tertiary, error, warning, success, informative) has only 10 (0, 100, 200 … 900): the extra half-steps exist purely so the three contrast tiers have somewhere finer to land on the neutral ramp. Component colour, surface and border tokens step further down the base ladder as the tier goes from Standard to High.
- **Text scale** — the six modes of **Raw Font Size Values** (1X through 2X), a straight linear multiplier, feeding into Typography Useable Tokens' Font Sizes group.
- **Language / script** — Language Switch's three modes, currently a placeholder: English, Arabic and Hindi all point at the same "Roman" font family and LTR direction. No RTL or non-Latin metrics exist yet.

## 4. Group trees

**Typography Useable Tokens** (32)
`Font Family (2)`, `Font Sizes (21)`, `Font Weights (9)`

**Raw Spacing Values** (23) and **Raw Font Size Values** (21) and **Language Switch** (2): flat, no subgroups.

**Lanuguage Collection** (2): `Roman (2)`

**Color Mode Switch** (90): `base (20)`, `primary (10)`, `secondary (10)`, `tertiary (10)`, `error (10)`, `warning (10)`, `success (10)`, `informative (10)`

**Raw Colors Values** (130): `neutral (20)`, `cool (20)`, `warm (20)`, `blue (10)`, `green (10)`, `red (10)`, `orange (10)`, `purple (10)`, `teal (10)`, `warm green (10)`

**Semantic Tokens** (142), mirrored exactly across onLight/onDark:
`surface (6+6)`, `layer (6+6)`, `on-fill (2+2)`, `border (4+4)`, `action/primary (9+9)`, `action/secondary (9+9)`, `action/neutral (9+9)`, `chart (10+10)`, `status/error (4+4)`, `status/warning (4+4)`, `status/success (4+4)`, `status/info (4+4)`

**Component Tokens** (141): `Atoms/Button` (2, the Active-Menu pair) plus four variant families each split Fill/Ghost (7 each): `Atoms/Button/Primary`, `/Secondary`, `/Neutral`; `Atoms/Chip/Primary`, `/Success`, `/Error` (4 each); `Atoms/Input Field` (6) and `Atoms/Input Field/Text` (2); `Atoms/Radio & Check` (5); then flat groups `Background (2)`, `Layer (3)` plus `Layer/Highlighted (2)`, `Border (4)`, `Information (8)`, `Status (8)`, `Chart (9)`, `Notification (2)`, `Search (4)`, `Card-Stat (8)`, `Sidebar (4)` plus `Sidebar/Tab (6)`.

**Screen Size Switch** (130): mirrors the same component families for typography and spacing (`Atoms/Buttons/Large`, `/Small`, `Atoms/Chip`, `Atoms/Input Field/Label`, `/Place Holder`, `/Helper text`, `Atoms/Radio & Check`), plus layout groups (`Page`, `Section`, `Dashboard/Side Nav`, `/Top Nav`, `/Central`, `Table/Min-Width`, `Typography/Text Styles/Heading`, `/Body`, `/Label`), plus **7 ungrouped root tokens** with no folder at all: `Screen Width Max`, `Screen Width Min`, `Screen Minimum Height`, `Presentation`, `Screen` (a string, values "Mobile"/"Desktop"/"Desktop"), `Mobile 1` and `Desktop 1` (booleans, Tablet mirrors Desktop on both). These three look built for binding to a component's variant properties rather than to a layer fill or gap, which matters for the bound-layer numbers below.

## 5. Typography

16 text styles, no orphans, every one binds `fontSize`, `fontFamily` and `fontWeight` to a Screen Size Switch variable (never a hard-coded number). They draw from three families in Screen Size Switch, Heading / Body / Label, each with its own Size and Weight sub-scale:

| Style | Size token | Family token | Weight token |
| --- | --- | --- | --- |
| Page/Title | Heading/Size/XS | Heading/Font Family | Heading/Weight/Thick |
| Page/Subtitle | Body/Size/L | Body/Font Family | Body/Weight/Default |
| Section/Title | Body/Size/XL | Body/Font Family | Body/Weight/Thick |
| Data/Metric/Primary | Heading/Size/L | Heading/Font Family | Heading/Weight/Thick |
| Data/Metric/Secondary | Heading/Size/XS | Heading/Font Family | Heading/Weight/Thick |
| Data/Metric/Compact | Body/Size/XL | Body/Font Family | Body/Weight/Thick |
| Body/Default | Body/Size/M | Body/Font Family | Body/Weight/Default |
| Body/Emphasis | Body/Size/M | Body/Font Family | Body/Weight/Medium |
| Body/Small | Body/Size/S | Body/Font Family | Body/Weight/Default |
| Table/Column-Header | Label/Size/S | Label/Font Family | Label/Weight/Medium |
| Table/Cell | Body/Size/S | Body/Font Family | Body/Weight/Default |
| Table/Cell-Emphasis | Body/Size/S | Body/Font Family | Body/Weight/Thick |
| Label/Default | Label/Size/L | Label/Font Family | Label/Weight/Medium |
| Label/Caption | Label/Size/S | Label/Font Family | Label/Weight/Medium |
| Label/Micro | Label/Size/XS | Label/Font Family | Label/Weight/Medium |
| Link/Default | Body/Size/M | Body/Font Family | Body/Weight/Medium |

The Heading family renders in DM Sans (Page/Title, Data/Metric/Primary and Secondary); Body and Label render in Inter. Because size and weight route through Screen Size Switch, resizing the canvas from Mobile to Desktop moves every one of these 16 styles automatically. The text-scale multiplier (Raw Font Size Values) sits one layer further down, under Typography Useable Tokens, and isn't touched directly by the text styles.

## 6. Effects

None. `getLocalEffectStylesAsync()` returned zero effect styles. Nothing in the file defines a shadow, blur or glass/clay treatment as a reusable style. If effects exist visually anywhere in the design, they're set per layer rather than as a named, reusable token, or they haven't been built yet.

## 7. Frames

Of 65 top-level frames, sections and components across the four pages, only 10 carry an explicit mode override; everything else inherits each collection's default mode (Light, Mobile, Cool, Standard, English).

| Page | Frame | Explicit modes |
| --- | --- | --- |
| Important Page | Component Kit Sheet — Quick Reference | Component Tokens: Light, Screen Size Switch: Desktop |
| Important Page | Onboarding Flow · v4 · Split Panel | Component Tokens: Light, Screen Size Switch: Mobile |
| Important Page | Onboarding Flow · Finch · Split Layout | Component Tokens: Dark |
| Important Page | GamePlan | *(unresolvable, see below)* |
| design | Made by Claude at - 2026-07-19 *(section)* | Color Mode Switch: Cool, plus unresolvable |
| design | LE Terminal · Dashboard | Component Tokens: Dark, Screen Size Switch: Desktop, Color Mode Switch: Cool, plus unresolvable |
| design | Made by Claude at - 2026-07-19 Investments *(section)* | Color Mode Switch: Cool, plus unresolvable |
| design | Made by Claude at - 2026-08-01 10:30 *(section)* | Color Mode Switch: Cool, plus unresolvable |
| design | Frame 2 | Color Mode Switch: Cool, plus unresolvable |
| design | Global Portfolio · Dashboard | Component Tokens: Light, Screen Size Switch: Desktop, Color Mode Switch: Cool, Raw Font Size Values: 1X, Semantic Tokens: Standard |

"Global Portfolio · Dashboard" is the only frame that pins all five switches at once, including the contrast tier and text scale; everything else pins one or two and leaves the rest on default. See anomaly below on the "plus unresolvable" entries: five frames on the `design` page carry a mode override into a variable collection this file doesn't own locally.

## 8. Anomalies

- **Typo, as given:** collection named **"Lanuguage Collection"** (missing an "e", should presumably read "Language Collection"). Left exactly as it appears in Figma, per instructions.
- **Likely typo, spacing names:** `Raw Spacing Values` has five tokens named with a percent sign standing in for a decimal point: **`S%50`** (value 2), **`S1%50`** (6), **`S2%50`** (10), **`S3%50`** (14), **`S4%50`** (18). Every neighbouring step reads as a clean number (S1=4, S2=8, S3=12, S4=16, S5=20), so these five look like they were meant to read "S0.5", "S1.5", "S2.5", "S3.5", "S4.5" and lost the decimal point in favour of a percent sign somewhere along the way.
- **Wrong code syntax:** `Typography Useable Tokens / Font Sizes/72` carries the WEB code syntax `var(--font-size-font-sizes-64)`, copy-pasted from the 64 token instead of reading "-72". If code generation trusts `codeSyntax` as the CSS variable name, the 72 size would silently collide with the 64 one.
- **`figma.root.name` reads "Document", not "TEST NEW".** I've used the file's browser-tab title ("TEST NEW", from the URL) in the JSON's `file.name` field, but the plugin API itself doesn't return that title; flagging in case the real file name matters downstream.
- **Two frame-level mode overrides point at variable collections outside this file's ten:** collection ids `776f040c1d20e1262ad26f90f9a6df4028bf1397/2196:67` (on "GamePlan") and `86482baec574d62a05b320256db1de4e2d33605a/368:370` (on five frames on the `design` page, always set to a mode whose id happens to be `138:0`, the same id Color Mode Switch uses for "Warm", though it's a different collection). These are references to a linked library file, not to anything local, so I can't resolve their real names or mode labels in a read-only pass on this file alone. On the five `design`-page frames, this remote override sits **alongside** a local `Color Mode Switch: Cool` override on the very same frame, so the frame is asking for "Cool" locally while also carrying what looks like a leftover pointer at a differently-sourced, possibly-Warm switch from another file. Worth reconciling.
- **Direct, layer-level bindings to a second, external variable source:** walking all 12,394 nodes across the four pages, 233 of this file's own 713 variables are bound to at least one layer, but I also found **3,810 bindings to 40 distinct variable ids that don't belong to any of this file's ten collections** (mostly on "Important Page", a handful on "design"). Those are almost certainly variables from a linked library. I didn't attempt to resolve them (would need that library's own file open), but it means a meaningful slice of what's actually built in this file draws on tokens outside this export.
- **Raw values used directly, bypassing the semantic layer, in two places:** `Color Mode Switch / primary/600` has 4 direct layer bindings despite Color Mode Switch normally being consumed only through Semantic Tokens; and 10 of the 23 `Raw Spacing Values` (S%50, S1, S1%50, S2, S2%50, S3, S4, S5, S8, S16) are bound directly to layers despite Raw Spacing Values normally being consumed only through Screen Size Switch. Everywhere else, the raw and intermediate layers (Raw Colors Values, Semantic Tokens, Typography Useable Tokens, Raw Font Size Values, both language collections) have **zero** direct bindings, meaning layers only ever reach them through Component Tokens or Screen Size Switch as intended. These few exceptions look like a handful of shortcuts taken directly to a raw or switch value, worth a design-side look.
- **No exact-duplicate names, no broken aliases, no cross-wired Light/Dark:** checked and clean. Every Component Tokens and Semantic Tokens colour variable is a pure alias (never a raw hex sitting next to aliased siblings), and no Dark-mode alias accidentally points at an `onLight/…` token or vice versa.
- **Bound-layer counts likely undercount real usage.** The scan reads each node's `boundVariables` (fills, strokes, spacing, sizing, text properties), which is what the brief asked for, but it can't see a variable bound to a **component's own boolean or variant property** (for example `Mobile 1` / `Desktop 1` / `Screen`, all three of which show 0 bound layers despite looking purpose-built for exactly that), nor per-character text overrides inside mixed-style text. Treat the "zero bound layers" list below as "not bound to a plain layer property on these four pages", not as proof nothing references the token.

**Collections and tokens with zero bound layers** (against the caveat just above):
- Semantic Tokens (142/142), Raw Colors Values (130/130), Typography Useable Tokens (32/32), Raw Font Size Values (21/21), Language Switch (2/2) and Lanuguage Collection (2/2) are **entirely** unbound. This reads as intentional: these six collections are pure intermediate/abstraction layers, consumed only by aliasing, never bound to a layer directly. Not a defect.
- Color Mode Switch: 89 of 90 unbound (only `primary/600` is bound; see above).
- Component Tokens: 14 of 141 unbound: `Atoms/Button/Active-Menu-BG`, `Atoms/Button/Active-Menu-Text`, `Atoms/Input Field/Hover`, `Layer/Layer 2`, `Layer/Layer 3`, `Information/Disabled`, `Border/Strong`, `Border/Focus`, `Status/Error-Subtle`, `Status/Warning`, `Status/Warning-Subtle`, `Status/Info`, `Status/Info-Subtle`, `Notification/Badge-Text`. These are candidates for "designed but not yet placed anywhere in these four pages."
- Screen Size Switch: 35 of 130 unbound, concentrated in the Dashboard/Central and Dashboard/Top Nav spacing groups, a handful of Heading/Body/Label sub-scale steps, and the seven root-level breakpoint/flag tokens (see typography caveat above for why the last three of those are probably used, just not visibly).
- Raw Spacing Values: 13 of 23 unbound (the larger steps, S6 and up, plus two of the five ".5" tokens).

## 9. Open questions

- What are the real names of the two remote/library variable collections referenced by frame mode-overrides (ids `776f040c1d20e1262ad26f90f9a6df4028bf1397/2196:67` and `86482baec574d62a05b320256db1de4e2d33605a/368:370`), and of the 40 remote variable ids bound directly to layers? Answering this needs the source library file open, which is outside a read-only pass on this file.
- Is the true file name "TEST NEW", or something else? The Plugin API returned "Document" for `figma.root.name`.
- Are the five `S%50`-style spacing names an intentional convention, or should they read "S0.5" etc.? And is `Font Sizes/72`'s code syntax a live bug or already known?
- Is the direct use of `Color Mode Switch/primary/600` and the ten direct `Raw Spacing Values` bindings deliberate shortcuts, or drift to clean up?
- Are the 14 unbound Component Tokens and 35 unbound Screen Size Switch tokens genuinely unused, or bound to nodes/pages outside the four scanned (there are only four pages in the file, so this would mean inside a component-property or text-override path the scan can't see)?
- Are shadows/glass/clay effects handled per layer on purpose, or still to be designed as reusable effect styles?

## Verification, as requested

- **Counts:** all ten collections match the Variables panel exactly (Component Tokens 141, Screen Size Switch 130, Language Switch 2, Typography Useable Tokens 32, Color Mode Switch 90, Raw Colors Values 130, Raw Spacing Values 23, Raw Font Size Values 21, Lanuguage Collection 2, Semantic Tokens 142; 713 total, RunTime's 1 excluded).
- **Aliases:** all resolve. Checked every alias's target id against the full 713-variable set; zero unresolved, zero marked broken by Figma itself.
- **Modes:** every variable carries a value for every mode of its own collection; zero gaps.
