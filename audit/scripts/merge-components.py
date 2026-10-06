#!/usr/bin/env python3
"""
Merge raw component-tree exports (JSON files in ../raw-components/) into
audit/components.json, resolving every VariableID reference to its
(collection, name) pair against ../figma-variables.json.

Read only: this script never talks to Figma. Run:
    python3 merge-components.py
"""
import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(SCRIPT_DIR, "..")
RAW = os.path.join(AUDIT, "raw-components")

data = json.load(open(os.path.join(AUDIT, "figma-variables.json")))
by_id = {v["id"]: v for v in data["variables"]}
unresolved = set()

def resolve(alias_id):
    if alias_id is None:
        return None
    v = by_id.get(alias_id)
    if not v:
        unresolved.add(alias_id)
        return {"collection": None, "name": None, "unresolvedId": alias_id}
    return {"collection": v["collection"], "name": v["name"]}

def load(name):
    return json.load(open(os.path.join(RAW, name)))

props = load("00-property-definitions.json")

# ---------------------------------------------------------------------------
# Buttons
# ---------------------------------------------------------------------------
buttons_bindings = load("08-buttons-all24-bindings.json")["variants"]
buttons_sample = load("01-buttons-sample-tree.json")["tree"]

def button_variant_entry(v):
    prop_values = dict(part.split("=") for part in v["name"].split(", "))
    return {
        "name": v["name"],
        "propValues": prop_values,
        "bindings": {
            "root": {
                "gap": resolve(v["root"]["itemSpacing"]),
                "paddingInline": resolve(v["root"]["paddingH"]),
                "paddingBlock": resolve(v["root"]["paddingV"]),
                "borderRadius": resolve(v["root"]["cornerRadius"]),
                "borderWidth": resolve(v["root"]["borderWidth"]),
                "background": resolve(v["root"]["fill"]),
                "borderColor": resolve(v["root"]["border"]),
            },
            "leadingIcon": {
                "size": resolve(v["icon"]["size"]) if v["icon"] else None,
                "color": resolve(v["icon"]["iconColor"]) if v["icon"] else None,
            },
            "label": {
                "color": resolve(v["text"]["fill"]) if v["text"] else None,
                "fontSize": resolve(v["text"]["fontSize"]) if v["text"] else None,
                "fontFamily": resolve(v["text"]["fontFamily"]) if v["text"] else None,
                "fontWeight": resolve(v["text"]["fontWeight"]) if v["text"] else None,
            },
            "focusRing": {
                "borderRadius": resolve(v["ring"]["cornerRadius"]) if v["ring"] else None,
                "borderWidth": resolve(v["ring"]["strokeWidth"]) if v["ring"] else None,
                "borderColor": resolve(v["ring"]["stroke"]) if v["ring"] else None,
                "offset": {"x": v["ring"]["x"], "y": v["ring"]["y"]} if v["ring"] else None,
                "strokeAlign": v["ring"]["strokeAlign"] if v["ring"] else None,
            } if v["ring"] else None,
        },
    }

buttons = {
    "name": "Buttons",
    "figmaId": props["Buttons"]["id"],
    "variantAxes": {k: vv["variantOptions"] for k, vv in props["Buttons"]["propertyDefinitions"].items() if vv["type"] == "VARIANT"},
    "otherProperties": [
        {"figmaKey": "Button#21:0", "type": "TEXT", "default": "Button", "appliesTo": "the label layer's characters"},
        {"figmaKey": "Leading Icon#25:25", "type": "BOOLEAN", "default": True, "appliesTo": "visibility of the leading icon slot (layer 'bx-refresh' in this file)"},
        {"figmaKey": "Tailing Icon#25:50", "type": "BOOLEAN", "default": False, "appliesTo": "visibility of the trailing icon slot (layer 'bx-rewind' in this file)"},
        {"figmaKey": "Leading icon#25:75", "type": "INSTANCE_SWAP", "appliesTo": "which icon component fills the leading slot"},
        {"figmaKey": "Tailing Icon2#25:100", "type": "INSTANCE_SWAP", "appliesTo": "which icon component fills the trailing slot"},
        {"figmaKey": "Focus#4021:0", "type": "BOOLEAN", "default": False, "appliesTo": "visibility of the focus-ring rectangle ('Rectangle 13')"},
    ],
    "layers": {
        "root": {"figmaType": "COMPONENT", "autoLayout": {"direction": buttons_sample["layoutMode"], "primaryAlign": buttons_sample["primaryAxisAlignItems"], "counterAlign": buttons_sample["counterAxisAlignItems"], "sizing": "HUG both axes"}, "strokeAlign": buttons_sample["strokeAlign"]},
        "leadingIcon": {"figmaType": "INSTANCE", "note": "square icon; only one dimension (width) is bound, the other follows the icon's own aspect ratio"},
        "label": {"figmaType": "TEXT", "figmaName": "Button", "note": "no named text style; fontSize/fontFamily/fontWeight are bound directly"},
        "focusRing": {"figmaType": "RECTANGLE", "figmaName": "Rectangle 13", "layoutPositioning": "ABSOLUTE", "offset": {"x": -4, "y": -4}, "sizeDelta": {"width": 8, "height": 8}, "note": "offset and size-delta are the same at both sizes: -4px/+8px. strokeAlign INSIDE. Colour and width are hardcoded to Primary's Ghost/Border regardless of the button's own Type (verified across all 24 variants, not per-type)."},
    },
    "variants": [button_variant_entry(v) for v in buttons_bindings],
}

# ---------------------------------------------------------------------------
# Icon-Buttons
# ---------------------------------------------------------------------------
iconbuttons_bindings = load("09-icon-buttons-all24-bindings.json")["variants"]
iconbuttons_sample = load("02-icon-buttons-sample-tree.json")["tree"]

def iconbutton_variant_entry(v):
    prop_values = dict(part.split("=") for part in v["name"].split(", "))
    return {
        "name": v["name"],
        "propValues": prop_values,
        "bindings": {
            "root": {
                "gap": resolve(v["root"]["itemSpacing"]),
                "paddingInline": resolve(v["root"]["paddingH"]),
                "paddingBlock": resolve(v["root"]["paddingV"]),
                "borderRadius": resolve(v["root"]["cornerRadius"]),
                "borderWidth": resolve(v["root"]["borderWidth"]),
                "background": resolve(v["root"]["fill"]),
                "borderColor": resolve(v["root"]["border"]),
            },
            "icon": {
                "size": resolve(v["icon"]["size"]) if v["icon"] else None,
                "color": resolve(v["icon"]["iconColor"]) if v["icon"] else None,
            },
            "focusRing": None,
        },
    }

iconbuttons = {
    "name": "Icon-Buttons",
    "figmaId": props["Icon-Buttons"]["id"],
    "variantAxes": {k: vv["variantOptions"] for k, vv in props["Icon-Buttons"]["propertyDefinitions"].items() if vv["type"] == "VARIANT"},
    "otherProperties": [
        {"figmaKey": "Icon#25:75", "type": "INSTANCE_SWAP", "appliesTo": "which icon component fills the button"},
    ],
    "layers": {
        "root": {"figmaType": "COMPONENT", "autoLayout": {"direction": iconbuttons_sample["layoutMode"], "sizing": "HUG both axes"}, "note": "paddingInline and paddingBlock both bind to the SAME 'Spacing/Equal' token per size (the button is square), not to Screen Size Switch's Horizontal/Vertical pair that Buttons uses."},
        "icon": {"figmaType": "INSTANCE", "note": "square icon; only one dimension bound, as in Buttons"},
    },
    "notes": ["Icon-Buttons has no Focus property and no focus-ring rectangle in Figma, in any of its 24 variants. No focus ring is built for it; this is an absence, not an oversight."],
    "variants": [iconbutton_variant_entry(v) for v in iconbuttons_bindings],
}

# ---------------------------------------------------------------------------
# Chip
# ---------------------------------------------------------------------------
chip_bindings = load("10-chip-all6-and-inputfield-focused-placeholder.json")["chips"]["variants"]
chip_sample = load("03-chip-sample-tree.json")["tree"]

def chip_variant_entry(v):
    prop_values = dict(part.split("=") for part in v["name"].split(", "))
    return {
        "name": v["name"],
        "propValues": prop_values,
        "bindings": {
            "root": {
                "gap": resolve(v["root"]["itemSpacing"]),
                "paddingInline": resolve(v["root"]["paddingH"]),
                "paddingBlock": resolve(v["root"]["paddingV"]),
                "borderRadius": resolve(v["root"]["cornerRadius"]),
                "borderWidth": resolve(v["root"]["borderWidth"]),
                "background": resolve(v["root"]["fill"]),
                "borderColor": resolve(v["root"]["border"]),
            },
            "icon": {
                "size": resolve(v["icon"]["size"]) if v["icon"] else None,
                "color": resolve(v["icon"]["iconColor"]) if v["icon"] else None,
            },
            "label": {
                "color": resolve(v["text"]["fill"]) if v["text"] else None,
                "fontSize": resolve(v["text"]["fontSize"]) if v["text"] else None,
                "fontFamily": resolve(v["text"]["fontFamily"]) if v["text"] else None,
                "fontWeight": resolve(v["text"]["fontWeight"]) if v["text"] else None,
            },
        },
    }

chip = {
    "name": "Chip",
    "figmaId": props["Chip"]["id"],
    "variantAxes": {k: vv["variantOptions"] for k, vv in props["Chip"]["propertyDefinitions"].items() if vv["type"] == "VARIANT"},
    "otherProperties": [
        {"figmaKey": "Chip#26:191", "type": "TEXT", "default": "Chip", "appliesTo": "the label layer's characters"},
        {"figmaKey": "icon#318:0", "type": "BOOLEAN", "default": True, "appliesTo": "visibility of the icon slot"},
    ],
    "layers": {
        "root": {"figmaType": "COMPONENT", "autoLayout": {"direction": chip_sample["layoutMode"], "sizing": "HUG both axes"}},
        "icon": {"figmaType": "INSTANCE", "figmaName": "bx-user (example icon)", "note": "size binds to Atoms/Chip/Spacing/Icon Size via the icon's HEIGHT only, same as Radio & Check's tick mark (a shared token, not Chip-specific)"},
        "label": {"figmaType": "TEXT", "figmaName": "Chip", "note": "no named text style; direct bindings, as in Buttons"},
    },
    "notes": ["No focus-ring rectangle in this component."],
    "variants": [chip_variant_entry(v) for v in chip_bindings],
}

# ---------------------------------------------------------------------------
# Input Field
# ---------------------------------------------------------------------------
if_filled = load("04-input-field-filled-tree.json")["tree"]
if_error_disabled = load("07-input-field-error-disabled.json")
if_focused_placeholder = load("10-chip-all6-and-inputfield-focused-placeholder.json")["inputField"]

def find_child(node, name):
    for c in node.get("children", []):
        if c["name"] == name:
            return c
    return None

def bv(node, key):
    b = (node or {}).get("boundVariables") or {}
    val = b.get(key)
    if val is None:
        return None
    if isinstance(val, list):
        val = val[0]
    if isinstance(val, dict) and "id" in val:
        return resolve(val["id"])
    if isinstance(val, str):
        return resolve(val)
    return None

def input_state_entry(state_name, root):
    frame2 = find_child(root, "Frame 2")
    frame1 = find_child(root, "Frame 1")
    frame3 = find_child(root, "Frame 3")
    label = find_child(frame2, "Label") if frame2 else None
    required = find_child(frame2, "*") if frame2 else None
    label_icon = find_child(frame2, "bx-user") if frame2 else None
    placeholder = find_child(frame1, "Placeholder") if frame1 else None
    leading_icon = find_child(frame1, "bx-user") if frame1 else None
    trailing_icon = find_child(frame1, "bx-calendar") if frame1 else None
    helper_icon = find_child(frame3, "bx-help-circle") if frame3 else None
    helper_text = find_child(frame3, "Helper Text") if frame3 else None
    return {
        "state": state_name,
        "bindings": {
            "labelRow": {
                "gap": bv(frame2, "itemSpacing"), "paddingInline": bv(frame2, "paddingLeft"), "paddingBlock": bv(frame2, "paddingTop"),
                "labelColor": bv(label, "fills"), "labelFontSize": bv(label, "fontSize"), "labelFontFamily": bv(label, "fontFamily"), "labelFontWeight": bv(label, "fontWeight"),
                "requiredMarkColor": bv(required, "fills"),
                "labelIconVisible": label_icon["visible"] if label_icon else None, "labelIconSize": bv(label_icon, "height"),
            },
            "fieldBox": {
                "gap": bv(frame1, "itemSpacing"), "paddingInline": bv(frame1, "paddingLeft"), "paddingBlock": bv(frame1, "paddingTop"),
                "borderRadius": bv(frame1, "topLeftRadius"), "borderWidth": bv(frame1, "strokeTopWeight"),
                "background": bv(frame1, "fills"), "borderColor": bv(frame1, "strokes"),
                "hasBorder": bool(frame1 and frame1.get("strokesCount")),
                "leadingIconVisible": leading_icon["visible"] if leading_icon else None, "leadingIconSize": bv(leading_icon, "height"), "leadingIconColor": bv(find_child(leading_icon, "Vector"), "fills") if leading_icon else None,
                "trailingIconVisible": trailing_icon["visible"] if trailing_icon else None, "trailingIconSize": bv(trailing_icon, "height"),
                "placeholderColor": bv(placeholder, "fills"), "placeholderFontSize": bv(placeholder, "fontSize"), "placeholderFontFamily": bv(placeholder, "fontFamily"), "placeholderFontWeight": bv(placeholder, "fontWeight"),
            },
            "helperRow": {
                "gap": bv(frame3, "itemSpacing"), "paddingInline": bv(frame3, "paddingLeft"), "paddingBlock": bv(frame3, "paddingTop"),
                "helperIconColor": bv(find_child(helper_icon, "Vector"), "fills") if helper_icon else None,
                "helperTextColor": bv(helper_text, "fills"), "helperFontSize": bv(helper_text, "fontSize"), "helperFontFamily": bv(helper_text, "fontFamily"), "helperFontWeight": bv(helper_text, "fontWeight"),
            },
        },
    }

input_field = {
    "name": "Input Field",
    "figmaId": props["Input Field"]["id"],
    "variantAxes": {k: vv["variantOptions"] for k, vv in props["Input Field"]["propertyDefinitions"].items() if vv["type"] == "VARIANT"},
    "otherProperties": [
        {"figmaKey": k, "type": v["type"], "default": v.get("defaultValue")}
        for k, v in props["Input Field"]["propertyDefinitions"].items() if v["type"] != "VARIANT"
    ],
    "layers": {
        "labelRow": {"figmaName": "Frame 2", "note": "holds Label, the '*' required mark, and an optional leading icon"},
        "fieldBox": {"figmaName": "Frame 1", "note": "the visible input box: leading icon, Placeholder text, trailing icon"},
        "helperRow": {"figmaName": "Frame 3", "note": "holds a help-circle icon and Helper Text"},
    },
    "notes": [
        "Frame 2 and Frame 3 share the SAME spacing tokens, named 'Atoms/Input Field/Label/Spacing/*', even though Frame 3 is the helper row, not a second label. A naming leftover in Figma (plan finding 6's 'leftover Spacing 2 group'), carried through as-is.",
        "Frame 1's own spacing tokens are named 'Atoms/Input Field/Place Holder/Spacing 2/*' (the 'Spacing 2' group finding 6 flagged).",
        "Filled state has no visible border (strokesCount 0) even though strokeWeight=1 is set; Focused and Error states DO show a border.",
        "Error state's field background binds to 'Atoms/Input Field/Disabled', the SAME token Disabled state uses, not a distinct 'Error' background. This looks like it may not be intentional: flagged for the report, not corrected.",
        "The input label's own font-family binds to the generic 'Typography/Text Styles/Label/Font Family' token, not an Input-Field-specific one, while its font-size and font-weight DO use Input-Field-specific tokens. Recorded exactly as bound.",
    ],
    "states": [
        input_state_entry("Filled", if_filled),
        input_state_entry("Focused", if_focused_placeholder["focused"]),
        input_state_entry("Placeholder", if_focused_placeholder["placeholder"]),
        input_state_entry("Disabled", if_error_disabled["disabled"]),
        input_state_entry("Error", if_error_disabled["error"]),
    ],
}

# ---------------------------------------------------------------------------
# Radio Button & Checkbox
# ---------------------------------------------------------------------------
rc_default = load("05-radio-checkbox-default.json")
rc_selected = load("06-radio-checkbox-selected-states.json")

def radio_check_state_entry(state_name, root):
    shape = find_child(root, "Radio Circle")
    label = find_child(root, "Label")
    tick = find_child(shape, "Tick Mark") if shape else None
    inner_fill = find_child(shape, "Inner Fill") if shape else None
    tick_vector = find_child(tick, "Vector") if tick else None
    return {
        "state": state_name,
        "bindings": {
            "gap": bv(root, "itemSpacing"),
            "shape": {
                "size": bv(shape, "height"), "borderRadius": bv(shape, "topLeftRadius"), "borderWidth": bv(shape, "strokeTopWeight"),
                "background": bv(shape, "fills"), "borderColor": bv(shape, "strokes"), "hasBorder": bool(shape and shape.get("strokesCount")),
            },
            "innerFill": {"color": bv(inner_fill, "fills")} if inner_fill else None,
            "tickMark": {"size": bv(tick, "height"), "color": bv(tick_vector, "fills")} if tick else None,
            "label": {"color": bv(label, "fills"), "fontSize": bv(label, "fontSize"), "fontFamily": bv(label, "fontFamily"), "fontWeight": bv(label, "fontWeight")},
        },
    }

radio = {
    "name": "Radio Button",
    "figmaId": props["Radio Button"]["id"],
    "variantAxes": {k: vv["variantOptions"] for k, vv in props["Radio Button"]["propertyDefinitions"].items() if vv["type"] == "VARIANT"},
    "otherProperties": [{"figmaKey": "Label#26:198", "type": "TEXT", "default": "Label"}],
    "layers": {"shape": {"figmaName": "Radio Circle", "figmaType": "FRAME", "note": "cornerRadius token makes it a full circle (20 at 16px = a circle)"}, "label": {"figmaType": "TEXT"}},
    "notes": [
        "Default: shape has fill + border, no inner content.",
        "Selected: shape keeps the SAME fill as Default but its border switches to 'Selected Fill' colour, and an 'Inner Fill' ellipse (dot) appears in that same colour. No tick icon.",
        "Selected Tick: shape has NO border; its fill becomes 'Selected Fill' (solid), and a 'Tick Mark' icon instance appears on top, coloured with the plain 'Fill' token (for contrast against the solid accent background).",
        "Tick Mark's size binds to 'Atoms/Chip/Spacing/Icon Size', a token from a different component's namespace, reused here rather than a Radio & Check-specific one.",
    ],
    "states": [
        radio_check_state_entry("Default", rc_default["radio"]["tree"]),
        radio_check_state_entry("Selected", rc_selected["radioSelected"]),
        radio_check_state_entry("Selected Tick", rc_selected["radioTick"]),
    ],
}

checkbox = {
    "name": "Checkbox",
    "figmaId": props["Checkbox"]["id"],
    "variantAxes": {k: vv["variantOptions"] for k, vv in props["Checkbox"]["propertyDefinitions"].items() if vv["type"] == "VARIANT"},
    "otherProperties": [{"figmaKey": "Label#26:198", "type": "TEXT", "default": "Label"}],
    "layers": {"shape": {"figmaName": "Radio Circle", "figmaType": "FRAME", "note": "layer keeps the name 'Radio Circle' even in the Checkbox set, a Figma authoring leftover; cornerRadius token makes it a rounded square, not a circle"}, "label": {"figmaType": "TEXT"}},
    "notes": [
        "Default: shape has fill + border (same Fill/Border tokens as Radio), no inner content.",
        "Selected: shape has NO border; fill becomes 'Selected Fill'; a 'Tick Mark' icon (checkmark) appears, coloured with the plain 'Fill' token.",
        "Intermediate: same as Selected, but the Tick Mark's inner vector is a flat dash shape (width 7, height 1) instead of a checkmark, same bindings otherwise.",
        "Shares Fill/Border/Selected Fill/Text/Border Width Component Tokens with Radio Button (one 'Atoms/Radio & Check/' namespace for both).",
    ],
    "states": [
        radio_check_state_entry("Default", rc_default["checkbox"]["tree"]),
        radio_check_state_entry("Selected", rc_selected["checkSelected"]),
        radio_check_state_entry("Intermediate", rc_selected["checkIntermediate"]),
    ],
}

# ---------------------------------------------------------------------------
# Assemble and write
# ---------------------------------------------------------------------------
result = {
    "sourcePage": "Important Page",
    "componentSets": [buttons, iconbuttons, chip, input_field, radio, checkbox],
}

variant_count = len(buttons["variants"]) + len(iconbuttons["variants"]) + len(chip["variants"])
state_count = len(input_field["states"]) + len(radio["states"]) + len(checkbox["states"])
print(f"[merge-components] Buttons: {len(buttons['variants'])} variants, Icon-Buttons: {len(iconbuttons['variants'])}, Chip: {len(chip['variants'])}")
print(f"[merge-components] Input Field: {len(input_field['states'])} states, Radio: {len(radio['states'])}, Checkbox: {len(checkbox['states'])}")
print(f"[merge-components] total variants/states covered: {variant_count + state_count} (expect 24+24+6+5+3+3=65)")
print(f"[merge-components] unresolved variable ids: {len(unresolved)}")
for u in unresolved:
    print("   UNRESOLVED:", u)

out_path = os.path.join(AUDIT, "components.json")
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)
print(f"[merge-components] wrote {out_path} ({os.path.getsize(out_path)} bytes)")
