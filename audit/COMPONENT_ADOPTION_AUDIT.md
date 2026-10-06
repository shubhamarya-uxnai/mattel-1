# Can Gradient Studio use the design system's components today?

23 September 2026. Measured against studio `v1.3.0` and `dist/components.css` (84 rules, CSS only, no JavaScript).

## The answer in a line

Four element types can move, covering about 19 of the studio's controls. They are not the controls the studio is made of, three states are missing that the studio actively uses, and every button would change size noticeably. Worth doing, but after the gaps close, not before.

## 1. What exists to adopt

`dist/components.css` offers six classes, all pure CSS on your tokens:

`.ds-button`, `.ds-icon-button`, `.ds-chip`, `.ds-field` (with `.ds-field-label`, `.ds-field-box`, `.ds-field-helper`), `.ds-checkbox`, `.ds-radio`.

Variants are set with data attributes, which is a clean fit for the studio's plain markup:
`data-size` large or small, `data-type` primary, secondary or neutral, `data-fill` on or off, and for chips `data-style` filled or ghost.

## 2. What can move today

| Studio element | Count | Moves to | Verdict |
| --- | --- | --- | --- |
| `.btn` and `.btn.sm` | 19 | `.ds-button[data-size][data-type][data-fill]` | Yes, but it resizes the panel. See section 3 |
| `.iconbtn` (gear, panel close) | 2 | `.ds-icon-button` | Yes, cleanest of the four |
| `.tbtn` (play and pause) | 1 | `.ds-icon-button` | Yes |
| Width and Height number inputs | 2 | `.ds-field` + `.ds-field-box` | Only with new markup, and it grows a lot |
| `.chip` | 0 | `.ds-chip` | Nothing to move, the class is dead CSS |
| Checkbox, radio | 0 | already exist | Studio uses toggle buttons instead |

Everything else in the studio has no component to move to. See section 5.

The variant mapping is straightforward:

| Studio | Design system |
| --- | --- |
| `.btn.sm` | `data-size="small" data-type="neutral" data-fill="on"` |
| `.btn` | `data-size="large" data-type="neutral" data-fill="on"` |
| `.btn.primary` | `data-type="primary" data-fill="on"` |
| `.btn.ghost` | `data-fill="off"` |

One extra step: `components.css` sizes icons through a `.ds-icon` class, and the studio's icons carry `.ph`. Every icon inside an adopted component needs both classes.

## 3. What it would change on screen

This is the part worth looking at before deciding. Measured, not estimated.

**Small buttons**, the studio's most common control, 16 of the 19:

| | Studio today | Design system | Change |
| --- | --- | --- | --- |
| Padding | 6px 9px | 8px 14px | Taller, and half again as wide |
| Text | 12px, weight 400 | 13px, weight 600 | Larger and much bolder |
| Corner | 14px | 10px | Noticeably squarer |
| Gap | 7px | 8px | Slightly wider |

**Large buttons**, the two main export buttons:

| | Studio today | Design system | Change |
| --- | --- | --- | --- |
| Padding | 8px 11px | 10px 18px | Much wider |
| Text | 13px, weight 600 | 18px, weight 500 | A third larger, and lighter |
| Corner | 14px | 14px | Unchanged |

**The number fields** would go from compact inline inputs to a 10px by 14px box with 18px text, roughly double their present height.

The pattern is consistent: your component sizes are built for content pages, where an 18px button label is right. The studio is a 274px control panel where the whole interface sits at 11 to 13px. Adopting the components as they stand would push the panels wider and force either a scroll or a narrower canvas.

**A conflict with the fonts you just chose.** The button and chip tokens carry their own font family, which resolves through `--ds-font-family-secondary` to Inter. `type.css` overrides `--font-sans`, not that token, so adopted components would render in Inter while everything around them stays Instrument Sans. One extra line in `type.css` fixes it, but it has to be deliberate.

## 4. What blocks it

Three states the studio uses every session simply do not exist in `components.css`:

- **Disabled buttons.** The browser export button disables itself when the engine is unavailable. There is no disabled rule for `.ds-button`, which is the D6 gap: the token was never made in Figma.
- **Selected chips.** The studio's `.chip.on` has no counterpart. Chips have type and style, no selected state. Moot today since chips are unused, but it blocks any future use.
- **The focus ring is still wrong.** The rule swaps the button's corner radius to Focus Radius on focus, on the belief that an outline cannot round its own corners. Measured at 8x in the browser: a plain outline with an offset gives an outer radius of 16.1, matching Figma's 16, while this version gives 19.9 and visibly rounds the button itself from 12 to 16. Adopting the components adopts that bug.

## 5. What the studio needs that the system does not have

This is the more useful finding. The studio is a real product running on your tokens, and it says plainly what the system is missing:

| Missing component | Studio uses | Why it matters |
| --- | --- | --- |
| **Slider** | 47 | The single most used control, and the one with the most states: value, hover, focus, disabled, and the filled track |
| **Select** | several | The other main control. Native selects are the hardest thing in any system to style consistently |
| **Accordion or panel** | 11 | Every group in both side panels |
| **Dialog** | 1 | The settings overlay |
| **Tabs** | 1 | Inside the settings overlay |

A slider and a select would cover more of this interface than every existing component combined, and both are far more reusable across your other work than another button variant.

## 6. Recommendation

**Do not adopt the buttons yet.** Nineteen controls would grow, the panel layout would need reworking, and three states the studio depends on are missing. The gain is consistency with components whose own sizing does not fit this product.

**A sensible order:**

1. **Move the two icon buttons and the transport button now** if you want a first real consumer of `components.css`. Three elements, no layout risk, and it proves the pipeline end to end.
2. **Close the three state gaps in Figma**: disabled button, selected chip, and the focus ring fix.
3. **Draw a slider and a select**, using the studio's own as the brief. This is where the value is.
4. **Then reconsider the buttons**, either by adding a third size below small, or by accepting that a dense tool panel uses the small size with its own padding.

Step 3 is the one that changes what your design system can do. The rest is tidying.

---

Related: `MAPPING_PLAN.md` decisions D6 (missing tokens) and D9 (focus ring). The studio's own notes are in `Gradient Creator/README.md`.
