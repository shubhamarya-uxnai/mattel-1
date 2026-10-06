# Design system: Figma to code, mapping plan

**Status:** D1 to D7 and D9 agreed on 22 Sep 2026; D8 stands as proposed. The pilot (run 2) passed on 22 Sep and was checked independently (section 10). Next is run 3, the full build.
**Source:** Figma file "TEST NEW" (`vtIMgD4yMz9PjMrif2OZu0`), audit of 22 Sep 2026: 713 variables in 10 collections (RunTime ignored), 16 text styles, no effect styles.
**Companion files in this folder:** `figma-variables.json` (the export), `STRUCTURE.md` (the audit report), `NAME_MAP.csv` (every Figma variable with its proposed code name).

---

## The plan in one minute

- **One code token for every Figma variable,** linked the same way and switching the same way. Nothing is typed twice. If a value changes in Figma, one export and one build carries it everywhere.
- **Every switch works like a mode on a Figma frame.** Set it on the page or on any element inside it, nest freely, in any combination. Anything not set is inherited from further out. This was tested in a browser today: dark, then high contrast inside it, then warm inside that, then light again inside that. All four came out as the exact Figma colours. Screen size and text scale passed the same test.
- **The page decides, not the visitor's system.** Every page starts from your Figma defaults (Light, Standard, Cool, 1X) and changes only what it sets itself. Screen size still follows the window width.
- **Three ways in:** plain CSS that works anywhere (Framer, Gradient Creator, any website), a Tailwind theme, and the shadcn names, so existing shadcn components and Gradient Creator pick up the system without changes.
- **The build proves itself.** Every token in every switch combination, more than 4,000 values, is compared with the value Figma itself gives, and every text and border pairing is checked for contrast. A mismatch fails the build.

---

## 1. What the audit tells us

The audit is clean and the structure is disciplined. These points change or shape the plan. Points 1 and 2 were not in `STRUCTURE.md`; I found them while planning.

1. **The code names written in Figma can't be used as they are.** 18 button tokens all carry the same code name, `--color-interactive-primary`, or its hover twin. 6 sidebar tab tokens all say `--color-sidebar-text`. 3 input field tokens reuse the Layer names. `warm green/0` says `-50`, and `Font Sizes/72` says `64`. So code names come from one naming rule applied to the Figma names instead (section 4). After the build, the correct names can be written back into Figma's code syntax, so Dev Mode shows them. That step writes to Figma, so it needs your go.
2. **One value is wrong, and it breaks readability.** `onDark/surface/overlay` at High contrast is `base/50`, near white, where Standard and Medium are `base/800`. In Dark + High, main text on Layer 3 (overlays) drops to **1.17:1**, which is unreadable. Following how the other dark surfaces step, it probably wants `base/850`. **Every other pairing I checked passes AA in all 12 colour combinations**, and contrast rises with each tier. That is 33 text and border pairings, from buttons and chips to inputs, borders and focus rings.
3. **Light and dark are perfectly paired.** All 127 component colours point at the same semantic token, under `onLight` in Light and under `onDark` in Dark. So in code, light and dark become a real switch, and nothing is lost.
4. **Some tokens are never reached** (kept in code, listed so you can decide):
   - the whole `neutral` raw ramp (20 colours): nothing points at it;
   - **pressed states:** the 6 `fill-pressed` semantic tokens have no component token, so no button has a pressed colour;
   - **disabled buttons:** no component token exists for them;
   - `chart/5` has no component token, and shadcn expects five chart colours;
   - warning and info text and border, 4 `surface-hover` tokens, and `chart/label`.
5. **"Layer" means two different things.** In Semantic Tokens, `layer/0` to `layer/5` are text colours. In Component Tokens, `Layer/Layer 1` to `Layer 3` are background surfaces. Code keeps your names, so it will carry the same double meaning; worth renaming one side in Figma.
6. **Small naming slips** that will show in code: `Atoms/Button` in Component Tokens but `Atoms/Buttons` in Screen Size Switch, a leftover `Spacing 2` group under Input Field, the `S%50` spacing names, and "Lanuguage Collection". None of them block anything. The collection typo never reaches code, and `S%50` becomes `0_5` by rule.
7. **Only headings follow the language switch.** Heading type goes through Language Switch; body and label type are fixed to Inter. Arabic or Hindi body text would stay in Inter. Also, all three languages currently point at the same Roman values.
8. **Screen sizes:** Tablet equals Desktop in all 130 tokens. Your frame widths (Mobile 390 to 440, Desktop 1080 to 1920) leave 441 to 1079 undefined, so code needs one breakpoint.
9. **Warm theme:** `secondary` and `error` use the same red ramp, and `tertiary` and `informative` the same purple ramp in both themes. In Warm, a secondary button and an error state look the same. That is a design call, not a code one; the 22 Aug audit of the earlier file flagged it too.
10. **Not in this file:** the colour vision modes and the glass (dark) and clay (light) surface styles. The switch mechanism takes new switches without re-planning anything else. Also, this file's frames use 40 variables from another library (3,810 bindings) and two remote collections. Code is built only from this file's own 713.

11. **The export missed some type details** (found after the pilot, from the text style specimen, node `73:641`). Table/Column-Header, Label/Caption and Label/Micro are set to uppercase, and Link/Default is underlined. The specimen uses exactly the 16 local text styles, no others. The export script is extended to record text case, decoration and paragraph settings from now on.
12. **Components have to be read from Figma, not guessed from token names.** The pilot gave the Large button's icon gap the Large Gap token (8 px), but the Figma button binds `S1` (4 px); the Large Gap token is bound nowhere. Each atom's own bindings are exported (`audit/components.json`) and the code follows them.

**Spacing already speaks Tailwind.** `S1` is 4 px, `S4` is 16 px, `S2%50` is 10 px. That is exactly Tailwind's spacing scale, where `p-4` is 16 px and `p-2.5` is 10 px, so Tailwind utilities land on your values with no translation.

---

## 2. Decisions to agree

| # | Decision | Proposed | Status |
| --- | --- | --- | --- |
| D1 | Follow the visitor's system settings when the page doesn't choose | **No.** Always start from the Figma defaults; only the page's own choice changes a switch. Sizes stay in pixels, as in Figma, so the browser's font size setting doesn't change them; browser zoom still enlarges everything | **agreed** |
| D2 | Where Mobile values give way to Desktop values | **768 px**, the usual tablet width, since Tablet already equals Desktop | **agreed** |
| D3 | Prefix on the design system's own names, to avoid clashes on other sites | **`ds`**, as in `--ds-color-background-page`; one setting, changeable before publishing | **agreed** |
| D4 | Can code use palette steps (like `primary/600`) directly? | **No:** only tokens that follow every switch are offered. Palette steps stay reachable underneath but aren't advertised, the same rule as binding component tokens in Figma | **agreed** |
| D5 | The overlay value (`onDark/surface/overlay` High is `base/50`) | **Left for now.** The full build goes ahead and its contrast check reports this one pair as a known failure until it's fixed in Figma | **agreed** |
| D6 | Add missing component tokens (pressed, disabled buttons, Chart 5) | **Later**, in Figma first; code never invents a colour | **agreed** |
| D7 | Components in the full build | **The atoms:** Buttons, Icon-Buttons, Chip, Input Field, Radio Button, Checkbox. Dashboard patterns later: Sidebar, Sidebar tabs, Top Navigation, Search, Card Stat, Notification | **agreed** |
| D8 | Write the code names back into Figma's code syntax | After the build, with your go | proposed |
| D9 | The focus ring | **As drawn in Figma** (section 8): a 1 px ring in `Primary/Ghost/Border`, 3 px out from the button, with Focus Radius corners, drawn as a real outline so it survives Windows high contrast. The pilot's shadow ring is replaced | **agreed** |

---

## 3. Layers

Each Figma collection becomes one layer in code, in the same order and with the same links.

| Figma collection | Code layer | Offered to designers and developers? | Switch it carries |
| --- | --- | --- | --- |
| Raw Colors Values (130) | raw colours | no, underneath | none |
| Color Mode Switch (90) | palette | no, underneath (D4) | Cool / Warm |
| Semantic Tokens (142) | semantic, `onLight` and `onDark` sets | no, underneath | contrast tier |
| Component Tokens (141) | **component colours and border widths** | **yes** | Light / Dark |
| Raw Spacing Values (23) | **spacing scale** | **yes**, as Tailwind's 4 px scale | none |
| Raw Font Size Values (21) | text sizes | no, underneath | text scale, 1X to 2X |
| Typography Useable Tokens (32) | type scale: families, sizes, weights | no, underneath (weights match Tailwind's) | none |
| Language Switch (2) and Lanuguage Collection (2) | language | no, underneath | follows the page's language |
| Screen Size Switch (130) | **responsive sizes:** type, spacing, radius, widths | **yes** | Mobile / Tablet / Desktop |
| 16 text styles | **type styles** | **yes** | through Screen Size Switch |

The offered layers match what you bind in Figma today: Component Tokens and Screen Size Switch cover nearly all of the 233 bound variables. The rest works underneath, reached only through links, as in Figma.

```
raw colours ──► palette (Cool/Warm) ──► semantic (contrast) ──► component colours (Light/Dark) ──► shadcn names
raw spacing ──────────────────────────────────────────────┐
raw text sizes (1X..2X) ──► type scale ◄── language ──────┴──► responsive sizes (screen) ──► type styles
```

---

## 4. Names

**One rule, no hand-picked names.** Anyone can work out a code name from the Figma name without a lookup table. The rule was run over all 713 variables: **713 names, 0 clashes.** The full list is in `NAME_MAP.csv`.

1. Start with the Figma name, for example `Atoms/Button/Primary/Fill/Fill`.
2. Drop or shorten the folders that only organise the panel: `Atoms/` is dropped, `Typography/Text Styles/` becomes `text`, and `Font Family/`, `Font Sizes/` and `Font Weights/` become `font-family`, `font-size` and `font-weight`.
3. Lowercase. Spaces and slashes become hyphens, `&` becomes `and`, and `%50` becomes `_5` (a half step).
4. Add the prefix (D3) and a word for the layer: `raw`, `palette`, `semantic`, `color` for component colours, `space` for the spacing scale, `raw-font-size`, `language` and `script`. Responsive sizes and component border widths need no extra word, because their names already say what they are.

| Figma | Code |
| --- | --- |
| Component Tokens / `Atoms/Button/Primary/Fill/Fill` | `--ds-color-button-primary-fill-fill` |
| Component Tokens / `Background/Page` | `--ds-color-background-page` |
| Component Tokens / `Atoms/Radio & Check/Border` | `--ds-color-radio-and-check-border` |
| Component Tokens / `Atoms/Button/Primary/Fill/Border Width` | `--ds-button-primary-fill-border-width` |
| Screen Size Switch / `Typography/Text Styles/Body/Size/M` | `--ds-text-body-size-m` |
| Screen Size Switch / `Atoms/Buttons/Large/Spacing/Horizontal` | `--ds-buttons-large-spacing-horizontal` |
| Screen Size Switch / `Section/Corner Radius` | `--ds-section-corner-radius` |
| Raw Spacing Values / `S4`, `S2%50`, `S%50` | `--ds-space-4`, `--ds-space-2_5`, `--ds-space-0_5` |
| Color Mode Switch / `primary/600` | `--ds-palette-primary-600` |
| Semantic Tokens / `onLight/action/primary/fill` | `--ds-semantic-onlight-action-primary-fill` |
| Raw Colors Values / `warm green/0` | `--ds-raw-warm-green-0` |
| Typography Useable Tokens / `Font Weights/SemiBold` | `--ds-font-weight-semibold` (Tailwind's own word) |
| Text style `Body/Default` | class `ds-type-body-default` |

Your Figma code syntax already used this shape where it was filled in correctly (`--color-background-page`, `--text-body-size-m`), so the rule keeps your intent and fixes the collisions.

---

## 5. Switches

| Switch | From Figma | In code | Options | Set by | Default |
| --- | --- | --- | --- | --- | --- |
| Light / Dark | Component Tokens modes | `data-theme`, also the `dark` class that shadcn and Gradient Creator use | `light`, `dark` | the page only (D1) | Light |
| Contrast | Semantic Tokens modes | `data-contrast` | `standard`, `medium`, `high` | the page only (D1) | Standard |
| Colour temperature | Color Mode Switch modes | `data-temperature` | `cool`, `warm` | the page only | Cool |
| Text scale | Raw Font Size Values modes | `data-text-scale` | `1`, `1.2`, `1.4`, `1.6`, `1.8`, `2` | the page only (D1) | 1 |
| Screen size | Screen Size Switch modes | `data-screen` | `mobile`, `tablet`, `desktop` | automatic from window width at 768 px (D2), or the page | automatic |
| Language | Language Switch modes | the page's own `lang` | `en`, `ar`, `hi` | the page language | English |

- **Nesting works like frames in Figma.** A dark sidebar in a light page, a high contrast preview inside a normal page, or a specimen showing every combination side by side all need nothing extra.
- **The visitor's system settings are not read** (D1). A visitor in system dark mode still sees Light until the page sets Dark. A page that wants to follow the system can add that itself later; the design system doesn't do it.
- **Text scale follows Figma exactly:** type grows, spacing stays, as in your Raw Font Size modes. Sizes are in pixels and match Figma to the pixel at every scale. The browser's font size setting doesn't change them; browser zoom still enlarges the whole page.
- **Direction:** Arabic pages set `dir="rtl"` themselves. Components use start and end spacing rather than left and right, so they mirror correctly. The Direction token is kept for reference.
- **High contrast mode on Windows** (forced colours) overrides every colour with the system's own. The system doesn't fight it. Components keep a real border, even when it's invisible, so shapes survive.
- **New switches later** (colour vision modes, glass and clay) are added as new attributes. Nothing else moves.

---

## 6. What the build produces

Everything lives in `~/building/design-system/`, next to this audit. It is published to a new GitHub repository only after asking. It is then served from jsDelivr by version tag, like Gradient Creator.

| File | What it is |
| --- | --- |
| `source/figma-variables.json` | the export, refreshed by re-running `audit/scripts/` |
| `build/build.mjs` | one script, no installs: reads the export and writes everything below |
| `dist/tokens.css` | every token and every switch. Works on any site, no framework needed |
| `dist/type.css` | the 16 type styles as classes (`ds-type-page-title`, and so on), including uppercase and underline where the style sets them |
| `dist/shadcn.css` | the shadcn and Gradient Creator names (section 7) |
| `dist/tailwind.css` | Tailwind theme: colours, type sizes, fonts, spacing, radius, breakpoint and type styles as utilities |
| `dist/components.css` | the atoms (D7) |
| `dist/fonts.css` | optional: loads DM Sans and Inter |
| `dist/tokens.json` | the same tokens in the W3C design tokens format, for other tools |
| `specimen/index.html` | every token, type style and atom, with switch controls, nested examples and the self check (section 9). Its type section repeats the Figma "Text Style Specimen" frame (node `73:641`) group by group, with the same sample text, so the two can be compared side by side |
| `README.md` | how to use it, written for designers first |

On a site: link `tokens.css`, `type.css` and `components.css`, and set switches as attributes. In Gradient Creator's Framer component: paste the `tokens.css` and `shadcn.css` links into the Design system box.

---

## 7. Compatibility names: shadcn and Gradient Creator

These names have no prefix, on purpose. That is how shadcn components and Gradient Creator already read colour. Each one points at a component token, so it follows every switch.

| Name | Points at | Note |
| --- | --- | --- |
| `--background` | Background/Page | |
| `--foreground` | Information/Primary | |
| `--card`, `--card-foreground` | Background/Card, Information/Primary | |
| `--popover`, `--popover-foreground` | Layer/Layer 2, Information/Primary | raised surface |
| `--primary`, `--primary-foreground` | Button Primary Fill: Fill, Text | |
| `--secondary`, `--secondary-foreground` | Layer/Layer 2, Information/Primary | shadcn's secondary is a quiet surface, not your teal ramp |
| `--muted` | Layer/Layer 2 | |
| `--muted-foreground` | Information/Secondary | |
| `--accent`, `--accent-foreground` | Button Neutral Ghost: Fill-Hover, Information/Primary | shadcn's hover fill |
| `--destructive`, `--destructive-foreground` | Status/Error, Chip Error Fill: Text | |
| `--border` | Border/Subtle | |
| `--input` | Input Field/Border | |
| `--ring` | Border/Focus | |
| `--chart-1` to `--chart-5` | Chart Primary, Secondary, Tertiary, Accent, and semantic `chart/5` | 5 has no component token yet (D6) |
| `--sidebar`, `--sidebar-foreground` | Sidebar/Background, Sidebar Tab Inactive-Text | |
| `--sidebar-primary`, `--sidebar-primary-foreground` | Button Primary Fill: Fill, Text | |
| `--sidebar-accent`, `--sidebar-accent-foreground` | Sidebar Tab: Active, Active-Text | |
| `--sidebar-border`, `--sidebar-ring` | Border/Subtle, Border/Focus | |
| `--radius` | Buttons Large: Border Radius | 12 px mobile, 14 px desktop |
| `--subtle-foreground` (Gradient Creator) | Information/Muted | hints and small print |
| `--highlight` (Gradient Creator) | Sidebar/Promo-Gradient-End | your own "second gradient colour" |
| `--success`, `--warning` (Gradient Creator) | Status/Success, Status/Warning | |
| `--primary-hover` (Gradient Creator) | Button Primary Fill: Fill-Hover | your hover, replacing the calculated shade |
| `--font-sans` (Gradient Creator) | Body font family | |

Gradient Creator works out its remaining shades itself (stage, transport, input hover, soft line, the primary button's edge and deep shades) from the names above, so they follow too. Its mono font stays its own, because the system has none.

---

## 8. How components use tokens

- **A component binds exactly what its Figma component binds,** layer by layer, read from `audit/components.json`. Never guessed from token names: the Large button's icon gap is `S1` (4 px) because that is what Figma binds.
- **Variant properties that describe the component become attributes,** named as in Figma: Buttons and Icon-Buttons take `data-size`, `data-type` and `data-fill`; Chip takes `data-type` and `data-style`. So `<button class="ds-button" data-size="large" data-type="primary" data-fill="on">`.
- **Variant properties that are interaction states become real states** of a real element, so keyboards and screen readers work without extra code:
  - Hover becomes hovering, and Focus or Focused becomes keyboard focus.
  - Disabled becomes the element's disabled state, and Error becomes `aria-invalid`.
  - Selected becomes checked, and Intermediate becomes the checkbox's mixed state.
  - Filled and Placeholder follow whether the field has text.
- **Boolean and icon-swap properties** (leading and trailing icons, helper text) become optional parts of the markup.
- **The focus ring is drawn as in Figma** (D9). It is the same in all 24 button variants: a ring box 4 px outside the button, with a 1 px line on its inside edge. That makes the gap 3 px, with corners on the Focus Radius token. Colour and width come from `Atoms/Button/Primary/Ghost/Border` and `Border Width`, for every type. In code it is an outline 3 px out, 1 px wide. Its corners follow the button's own radius plus 4 px, which equals Focus Radius at every size and screen. An outline, unlike a shadow, stays visible in Windows high contrast mode.
- **Every state it has in Figma, it has in code. States with no token in Figma are left out and listed, never invented.** Today that means pressed and disabled buttons (D6).
- **Start and end, not left and right,** so Arabic mirrors correctly.
- **Visible shapes in forced colours:** borders stay real (transparent when not wanted) so buttons keep their outline in Windows high contrast.

---

## 9. How the build proves it matches Figma

1. **Before writing anything:** 713 variables read, every link resolves, every mode has a value, every name is unique, no loops. Any failure stops the build.
2. **Every value, every combination.** The build works out, straight from the Figma export, what every offered token should be in each switch combination. That is 12 colour combinations (2 themes, 3 contrast tiers, 2 temperatures) and 18 size combinations (3 screens, 6 text scales). The specimen page then asks the browser what it actually gets, and compares: more than 4,000 values. Colours must match exactly; sizes within 0.01 px. The page shows "all match" or lists each difference. It runs in any browser, including your Arc.
3. **Contrast in every combination:** every text colour on the surface it's meant for (4.5:1) and every border and focus ring on its surface (3:1). It also flags any place where a higher contrast tier gives lower contrast. The one overlay pair is expected to fail and is shown as a known failure until it is fixed in Figma (D5); any other failure fails the check.
4. **Components match their Figma bindings:** for every variant of every atom, each styled property (fill, text, border, border width, padding, gap, radius, type, icon size, focus ring) equals the value of the token Figma binds, in every combination. The focus ring's corners equal Focus Radius at both sizes and both screen sizes.
5. **Nesting:** the specimen carries nested examples, like today's test, and checks them the same way.
6. **Visitor settings are ignored** (D1): with dark mode and "increase contrast" switched on in the browser, a page that sets nothing still shows Light and Standard.

---

## 10. Pilot slice (run 2)

One surface (Background/Card), its text (Information/Primary in the Body/Default style) and one primary filled large button, through every switch: 12 colour combinations, 18 size combinations, the nested examples, and a check that the visitor's settings are not read. It passes only if every value matches Figma exactly. If anything is off, this plan is corrected before the full build.

**Result, 22 Sep 2026: passed.** The pilot page shows 367 of 367 values matching Figma and 48 of 48 contrast pairs passing, at a narrow and a wide window. Opus checked it independently:
- **The rebuild** came out identical.
- **The whole token file,** not just the slice, was read back from the browser against Figma: all 127 component colours in 12 combinations, all 117 responsive numbers in 18 combinations, and 127 nested checks. There were 3,757 values and 0 differences.

Two fixes carry into run 3: the focus ring (D9) and the Large button's gap (finding 12).

## 11. Keeping in sync

When tokens change in Figma: re-run `audit/scripts/`, then the build. The build reports what was added, removed or changed since the last run, then runs all the checks. Only a change in structure comes back to planning: a new collection, a new mode or switch, or renamed folders that break the naming rule.

---

## Appendix A: the switch mechanism (for the builder)

Tested in Chromium on 22 Sep 2026 with real values from this file. Five nested colour cases, and forced mobile plus 1.4X inside an automatic desktop root, all matched.

**Why it's needed.** A CSS custom property that points at another one is worked out on the element where it is declared, and children inherit the finished value. A switch set on an inner element would change the bottom layer but not the layers built on it. So every layer above the constants is declared again on each element that carries a switch. The switches themselves travel down as inherited on and off values. An "on" value is the invalid value, so `var(--x, fallback)` picks its fallback; an "off" value is empty, so it adds nothing.

```css
/* on and off */
:root, :host { --ds-on: initial; --ds-off: ; }

/* defaults: Figma's default mode of each collection */
:root, :host {
  --ds-when-light: var(--ds-on); --ds-when-dark: var(--ds-off);
  --ds-when-standard: var(--ds-on); --ds-when-medium: var(--ds-off); --ds-when-high: var(--ds-off);
  --ds-when-cool: var(--ds-on); --ds-when-warm: var(--ds-off);
  /* likewise scale-1 ... scale-2, mobile / tablet / desktop, english / arabic / hindi */
}

/* screen size follows the window width where the page hasn't chosen (D2).
   No prefers-color-scheme or prefers-contrast rules: visitor settings are not read (D1). */
@media (min-width: 768px) { :root:not([data-screen]) { /* desktop on, others off */ } }

/* switches, on any element */
[data-theme="dark"], .dark { --ds-when-light: var(--ds-off); --ds-when-dark: var(--ds-on); }
[data-theme="light"], .light { --ds-when-light: var(--ds-on); --ds-when-dark: var(--ds-off); }
/* likewise data-contrast, data-temperature, data-text-scale, data-screen, and [lang|="en"], [lang|="ar"], [lang|="hi"] */

/* constants: declared once */
:root, :host { --ds-raw-blue-600: #0053d0; --ds-space-4: 16px; /* ... */ }

/* everything that depends on a switch: declared again wherever any switch is set */
:root, :host, [data-theme], .dark, .light, [data-contrast], [data-temperature], [data-text-scale], [data-screen], [lang] {
  --ds-palette-primary-600: var(--ds-when-cool, var(--ds-raw-blue-600)) var(--ds-when-warm, var(--ds-raw-warm-green-600));
  --ds-semantic-onlight-action-primary-fill: var(--ds-when-standard, var(--ds-palette-primary-600)) var(--ds-when-medium, var(--ds-palette-primary-700)) var(--ds-when-high, var(--ds-palette-primary-800));
  --ds-color-button-primary-fill-fill: var(--ds-when-light, var(--ds-semantic-onlight-action-primary-fill)) var(--ds-when-dark, var(--ds-semantic-ondark-action-primary-fill));
  color-scheme: var(--ds-when-light, light) var(--ds-when-dark, dark);
  /* ... */
}
```

Rules for writing it out:
- **Links stay links:** every Figma alias becomes a `var()` reference to its target; nothing is resolved.
- **A value that is the same in every mode** is written once, without switches.
- **A variable is a constant** only if its collection has one mode and everything it points at is constant. Constants go in the once-only block; everything else goes in the switch block.
- **Toggle names:** `--ds-when-` plus the Figma mode name, lowercased, with `.` written as `_` (`1.2X` becomes `--ds-when-scale-1_2`; the attribute value is `1.2`).
- **Units:** colours as hex (8 digits when alpha is below 1); font sizes, spacing, radius and widths in px, rounded to 4 decimals (13.1999998 px becomes 13.2px), because sizes don't follow the browser's font size setting (D1); font weights plain numbers; strings quoted. Font families get a fallback stack (`"DM Sans", ui-sans-serif, system-ui, sans-serif`); booleans become 1 and 0.
- **Type styles** take size, family and weight from their bound tokens. Line height, letter spacing, text case and decoration come from the style itself: 120% becomes `1.2`, -1% becomes `-0.01em`, UPPER becomes `text-transform: uppercase`, and UNDERLINE becomes `text-decoration: underline`.
- **Nothing is declared on elements without a switch.** The re-declaration happens only on switch elements, so the cost stays small.
- **Expected values** for the checks come from a separate, small resolver that walks the Figma export directly. It never reads the generated CSS, so the two can't share a mistake.

## Appendix B: Tailwind theme (for the builder)

Tailwind v4, following shadcn's pattern: the theme points at the system's names with `@theme inline`, so utilities read the live value on each element and switches keep working.

- **Colours:** `--color-<name>: var(--ds-color-<name>)` for the 127 component colours, for example `bg-button-primary-fill-fill`. The shadcn names are mapped too (`bg-background`, `text-foreground`, and so on).
- **Type:** `--font-heading`, `--font-body` and `--font-label` from the text family tokens; `--text-<family>-<step>` from `text/<family>/size/<step>`, for example `text-body-m`.
- **Spacing:** `--spacing: 4px`, so `p-4` is `S4`. Responsive gaps and paddings from Screen Size Switch become named spacing (`gap-page-gap`, `p-section-padding`), and radius tokens become `rounded-*`.
- **Other:** `--breakpoint-desktop: 768px`; `--font-weight-regular: 400` alongside Tailwind's own weights; the 16 type styles as `type-*` utilities; and a `dark` variant bound to `data-theme="dark"` and the `dark` class.
- Palette and raw tokens are not mapped (D4).
