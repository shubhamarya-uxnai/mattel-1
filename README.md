# Design system

Built from Figma file "TEST NEW" (`vtIMgD4yMz9PjMrif2OZu0`). Source file: https://www.figma.com/design/vtIMgD4yMz9PjMrif2OZu0

Every colour, size and name in here comes from that file: nothing is invented, and the build proves it against Figma every time it runs.

## For designers

This system has six switches. Nothing changes until a page sets one; a page that sets nothing looks exactly like your Figma defaults: Light, Standard contrast, Cool, 1X text, and whatever screen size the window implies.

| Switch | Values | Set with | Default |
| --- | --- | --- | --- |
| Theme | Light, Dark | `data-theme="dark"` or the `.dark` class | Light |
| Contrast | Standard, Medium, High | `data-contrast="high"` | Standard |
| Colour temperature | Cool, Warm | `data-temperature="warm"` | Cool |
| Text scale | 1, 1.2, 1.4, 1.6, 1.8, 2 | `data-text-scale="1.4"` | 1 |
| Screen size | Mobile, Tablet, Desktop | `data-screen="mobile"`, or leave it out | automatic, at 768px |
| Language | English, Arabic, Hindi | the page's own `lang` attribute | English |

Put a switch on `<html>` to change the whole page, or on any element inside it to change just that part: a dark sidebar in a light page, a high-contrast preview panel, whatever you need. Switches nest freely and in any order. The visitor's own system settings (dark mode, "increase contrast") are never read; only what the page itself sets matters.

**What's offered** (safe to reach for directly): the 127 component colours (`--ds-color-*`), the spacing scale (`--ds-space-*`), the responsive sizes and type styles that come from Screen Size Switch, and the 16 type styles as classes (`ds-type-body-default`, and so on). **What's underneath** (linked to automatically, not meant to be used directly): raw colours, the Cool/Warm palette, and the semantic layer. If you find yourself reaching for a palette step like `primary-600`, that usually means a component colour is missing in Figma rather than something to work around here.

## Adding it to a page

Plain HTML, Framer, or anywhere else that takes a `<link>` tag:

```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="type.css">
<link rel="stylesheet" href="components.css">
<link rel="stylesheet" href="fonts.css"> <!-- optional: skip if the site already loads Inter and DM Sans -->
```

When using the hosted global version, load from jsDelivr:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/shubhamarya-uxnai/mattel-1@main/dist/tokens.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/shubhamarya-uxnai/mattel-1@main/dist/type.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/shubhamarya-uxnai/mattel-1@main/dist/components.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/shubhamarya-uxnai/mattel-1@main/dist/shadcn.css">
```

Then use the tokens directly:

```css
.my-card {
  background-color: var(--ds-color-background-card);
  color: var(--ds-color-information-primary);
}
```

or the type classes and the atoms:

```html
<p class="ds-type-body-default">Body text, in the right size for the current screen and language.</p>
<button class="ds-button" data-size="large" data-type="primary" data-fill="on">
  <span class="ds-icon"><!-- an inline SVG icon --></span>
  <span>Continue</span>
</button>
```

## The atoms

Each atom's markup follows what it binds in Figma, not a guess from its name (`audit/components.json` has the exact bindings; see "How components use tokens" in `audit/MAPPING_PLAN.md` section 8). A few things worth knowing:

- **Buttons**: `data-size`, `data-type`, `data-fill` pick the look; hover is real `:hover`; the focus ring is a real `outline`, so it survives Windows high-contrast mode. Icons go in `<span class="ds-icon">`, sized and coloured by the button; drop in whatever icon SVG you like (`fill="currentColor"` on the SVG picks up the button's own text colour).
- **Icon-Buttons**: same pattern, no label. Figma has no focus-ring token for this one, so none is drawn; that's a gap in Figma, not something this build guessed around.
- **Chip**: `data-type`, `data-style`. One size.
- **Input Field**: a real `<input>` inside `.ds-field-box`; `Focused` is `:focus-within`, `Disabled` is the input's own `disabled` attribute, `Error` is `aria-invalid="true"` on the box. No separate "state" attribute to keep in sync by hand.
- **Radio Button / Checkbox**: a real `<input type="radio">` or `<input type="checkbox">`, visually hidden, next to a styled `.ds-shape`. Selected is the input's real `:checked` state; a checkbox's Intermediate is its real `indeterminate` property (set from script; CSS alone can't trigger it). Figma's radio has a third look, "Selected Tick" (a solid dot with a checkmark instead of an outline and a plain dot); since a native radio input only has two states, that look is an opt-in modifier, `data-mark="tick"`, on top of the same `:checked` state, not a third state of its own.
- **States Figma has no token for** (pressed and disabled buttons) are left out, not invented. They'll appear once Figma has them (plan D6).

Every property on every atom is checked against Figma directly, every time the build runs (see `specimen/index.html`).

## Three ways in

- **`tokens.css` + `type.css` + `components.css`**: plain CSS, works anywhere.
- **`tailwind.css`**: a Tailwind v4 theme (`@theme inline`), so `bg-button-primary-fill-fill`, `p-4`, `gap-page-gap`, `rounded-buttons-large-spacing-border-radius`, and the `type-*` utilities all read the live token. Written for Tailwind v4's CSS-first config; this build has no installs (Node built-ins only), so it hasn't been run through an actual Tailwind compile: check it compiles in your own project before relying on it.
- **`shadcn.css`**: the un-prefixed names (`--background`, `--primary`, `--radius`, and so on) that shadcn components and Gradient Creator already read. Load it after your other CSS; nothing else needs to change.

## Gradient Creator

In the Framer component's "Design system" field, add:

```
https://cdn.jsdelivr.net/gh/shubhamarya-uxnai/mattel-1@main/dist/tokens.css
https://cdn.jsdelivr.net/gh/shubhamarya-uxnai/mattel-1@main/dist/shadcn.css
```

(or `http://localhost:<port>/dist/...` while previewing locally, which the component explicitly allows). It reads exactly the same `--background` / `--card` / `--primary` names this system publishes, and applies on top of the studio's own styles because it loads them last. Set the `dark` prop for dark mode. This was tried directly against the running studio (not just read from source): the studio's own `--background`, `--card`, `--primary`, `--border`, `--ring`, `--radius` and `--font-sans` all switched to this system's Dark, Standard, Cool values the moment the two stylesheets were added, with no other change. See `BUILD_REPORT.md` for the exact before/after values.

## Keeping this in sync

When tokens or components change in Figma:

1. Re-run `audit/scripts/` (see its `README.md`): variables, text styles, and components as needed, then `python3 merge.py` and `python3 merge-components.py`.
2. Copy the refreshed `figma-variables.json` into `source/`.
3. Run `node build/build.mjs` and `node build/expected.mjs`.
4. Open `specimen/index.html` (through the `design-system-pilot` preview, not `file://`) and check that every check still passes.

Only a change in *structure* (a new collection, a new mode, a renamed folder that breaks the naming rule, `audit/MAPPING_PLAN.md` section 4) needs a conversation before the next build; a changed colour or size just flows through.

## For developers: what's in each file

| File | What it is |
| --- | --- |
| `source/figma-variables.json` | the export the build reads |
| `build/build.mjs` | the generator: checks the export's structure, names every token, writes everything in `dist/` |
| `build/expected.mjs` | an independent resolver for the checks; never reads generated CSS |
| `dist/tokens.css` | all 713 tokens, all six switches |
| `dist/type.css` | the 16 type styles as classes |
| `dist/components.css` | the six atoms |
| `dist/shadcn.css` | the shadcn / Gradient Creator names |
| `dist/tailwind.css` | the Tailwind v4 theme |
| `dist/fonts.css` | optional Google Fonts include (Inter, DM Sans) |
| `dist/tokens.json` | the same tokens, W3C design tokens format, for other tools |
| `dist/icons/*.svg` | Phosphor icons (MIT licensed) used by the specimen's atom examples, imported directly rather than recreating Figma's placeholder icon vectors, since those slots are instance-swappable in Figma anyway |
| `specimen/index.html` | every token, type style and atom, with switch controls, nested examples, and the self check |
| `audit/` | the read-only Figma audit this build is built from: `figma-variables.json`, `components.json`, `NAME_MAP.csv`, `CONTRAST_PAIRS.csv`, `MAPPING_PLAN.md`, `STRUCTURE.md`, and the re-runnable fetch scripts |

This repository is intended to be the shared hosted source for projects that need the design system. Prefer the jsDelivr URLs above over copying local CSS into each project.
