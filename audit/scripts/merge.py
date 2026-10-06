#!/usr/bin/env python3
"""
Merge raw Figma variable-collection exports (JSON files in ../raw/) into
figma-variables.json, and print a verification report.

Read only: this script never talks to Figma. It only reads the JSON files
that the fetch scripts in this folder produce, and writes one output file
one level up (../figma-variables.json).

Run:
    python3 merge.py

Expects ../raw/ to contain:
  00-overview.json                     (from 01-fetch-overview.js)
  <collection-slug>_<start>-<end>.json (from 02-fetch-variables-batch.template.js,
                                         one file per batch; see README)
  text-styles.json, effect-styles.json (from 03-fetch-styles.js)
  page-<page-name>.json                (from 04-fetch-page-scan.template.js,
                                         one file per page)
"""
import json, glob, os, re
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, "..", "raw")
OUT_DIR = os.path.join(SCRIPT_DIR, "..")

NON_VARIABLE_FILES = {
    "00-overview.json", "text-styles.json", "effect-styles.json",
}

def load(name):
    with open(os.path.join(RAW_DIR, name)) as f:
        return json.load(f)

def is_page_file(basename):
    return basename.startswith("page-")

overview = load("00-overview.json")
coll_by_id = {c["id"]: c for c in overview["collectionSummaries"]}
coll_by_name = {c["name"]: c for c in overview["collectionSummaries"]}
modeid_to_name = {}
for c in overview["collectionSummaries"]:
    for m in c["modes"]:
        modeid_to_name[(c["id"], m["modeId"])] = m["name"]

EXPECTED = {c["name"]: c["variableCount"] for c in overview["collectionSummaries"]
            if c["name"] != "RunTime"}

# ---- Load all variable batches (anything not overview/styles/pages) ----
variable_files = [os.path.basename(f) for f in glob.glob(RAW_DIR + "/*.json")
                   if os.path.basename(f) not in NON_VARIABLE_FILES
                   and not is_page_file(os.path.basename(f))]

all_vars = []
for f in sorted(variable_files):
    data = load(f)
    all_vars.extend(v for v in data.get("variables", []) if v and not v.get("missing"))

print(f"[merge] total variable records loaded: {len(all_vars)}")

ids_seen = defaultdict(int)
for v in all_vars:
    ids_seen[v["id"]] += 1
dupes = {k: n for k, n in ids_seen.items() if n > 1}
print(f"[merge] duplicate variable ids across batches: {len(dupes)}")
if dupes:
    print("        ", dupes)

# ---- Page scans: merge boundVariableCounts (local ids only) ----
page_files = [os.path.basename(f) for f in glob.glob(RAW_DIR + "/page-*.json")]
pages = [load(p) for p in page_files]
local_ids = set(v["id"] for v in all_vars)

bound_counts_local = defaultdict(int)
bound_counts_remote = defaultdict(int)
for p in pages:
    for vid, n in p.get("boundVariableCounts", {}).items():
        (bound_counts_local if vid in local_ids else bound_counts_remote)[vid] += n

print(f"[merge] local variables with >=1 bound layer: {len(bound_counts_local)} / {len(all_vars)}")
print(f"[merge] distinct REMOTE variable ids referenced by layers: {len(bound_counts_remote)}"
      f"  (total bindings: {sum(bound_counts_remote.values())})")

# ---- Frames with explicit modes ----
frames_out = []
remote_frame_collection_ids = set()
for p in pages:
    for fr in p.get("frames", []):
        if fr["explicitVariableModes"]:
            resolved = {}
            for cid, mid in fr["explicitVariableModes"].items():
                cname = coll_by_id.get(cid, {}).get("name")
                mname = modeid_to_name.get((cid, mid))
                if cname is None:
                    remote_frame_collection_ids.add(cid)
                    cname = f"<remote/unknown collection {cid}>"
                    mname = mname or f"<mode {mid}>"
                resolved[cname] = mname
            frames_out.append({"page": p["pageName"], "name": fr["name"], "explicitModes": resolved})

print(f"[merge] frames with explicit variable modes: {len(frames_out)}"
      f"  (remote/unresolvable collection ids: {len(remote_frame_collection_ids)})")

# ---- Build final variables[] ----
def clean_valuesByMode(vbm):
    out = {}
    for mode_name, val in vbm.items():
        if "value" in val:
            out[mode_name] = {"value": val["value"]}
        elif "alias" in val:
            out[mode_name] = {"alias": val["alias"], "aliasCollection": val["aliasCollection"], "aliasId": val["aliasId"]}
        else:
            out[mode_name] = val
    return out

broken_aliases = []
final_vars = []
for v in all_vars:
    for mode_name, val in v["valuesByMode"].items():
        if isinstance(val, dict) and val.get("broken"):
            broken_aliases.append((v["id"], v["name"], mode_name))
    final_vars.append({
        "id": v["id"], "name": v["name"], "collection": v["collection"], "type": v["type"],
        "description": v.get("description", ""), "scopes": v.get("scopes", []),
        "codeSyntax": v.get("codeSyntax", {}), "hiddenFromPublishing": v.get("hiddenFromPublishing", False),
        "valuesByMode": clean_valuesByMode(v["valuesByMode"]),
        "boundNodeCount": bound_counts_local.get(v["id"], 0),
    })

print(f"[merge] broken aliases found: {len(broken_aliases)}")
for b in broken_aliases:
    print("        BROKEN:", b)

# ---- Verify counts ----
count_by_collection = defaultdict(int)
for v in all_vars:
    count_by_collection[v["collection"]] += 1

print("\n[merge] === count verification vs Variables panel ===")
all_ok = True
for name, expected in EXPECTED.items():
    got = count_by_collection.get(name, 0)
    ok = got == expected
    all_ok &= ok
    print(f"  {name:30s} expected={expected:4d} got={got:4d}  {'OK' if ok else 'MISMATCH'}")

# ---- Verify every variable has a value for every mode of its collection ----
missing_mode_values = []
for v in all_vars:
    coll = coll_by_name[v["collection"]]
    expected_modes = set(m["name"] for m in coll["modes"])
    got_modes = set(v["valuesByMode"].keys())
    if expected_modes != got_modes:
        missing_mode_values.append((v["id"], v["name"], v["collection"], expected_modes - got_modes))
print(f"\n[merge] variables with mode-value mismatches: {len(missing_mode_values)}")
for m in missing_mode_values:
    print("        ", m)

# ---- Verify every alias resolves ----
id_set = set(v["id"] for v in all_vars)
unresolved_aliases = []
for v in all_vars:
    for mode_name, val in v["valuesByMode"].items():
        if isinstance(val, dict) and "alias" in val and val["aliasId"] not in id_set:
            unresolved_aliases.append((v["id"], v["name"], mode_name, val["aliasId"]))
print(f"\n[merge] aliases whose target id is NOT found among exported variables: {len(unresolved_aliases)}")
for u in unresolved_aliases:
    print("        ", u)

if not all_ok or missing_mode_values or unresolved_aliases:
    print("\n[merge] *** FIX THE ABOVE BEFORE TRUSTING THE OUTPUT ***")
    print("        Missing variables are almost always in ONE under-sized batch file.")
    print("        Compare its 'batchCount' field to len(variables) inside it to find the gap,")
    print("        then re-fetch just the missing id(s) with getVariableByIdAsync and drop a")
    print("        small extra JSON file (any name) with a top-level \"variables\": [...] array")
    print("        into ../raw/ before re-running this script.")

# ---- Write figma-variables.json ----
collections_out = []
for c in overview["collectionSummaries"]:
    if c["name"] == "RunTime":
        continue  # out of scope, per audit instructions
    default_mode_name = next((m["name"] for m in c["modes"] if m["modeId"] == c["defaultModeId"]), None)
    collections_out.append({
        "id": c["id"], "name": c["name"], "hiddenFromPublishing": c["hiddenFromPublishing"],
        "defaultMode": default_mode_name, "modes": [m["name"] for m in c["modes"]],
        "variableCount": c["variableCount"],
    })

text_styles_raw = load("text-styles.json")["textStyles"] if os.path.exists(os.path.join(RAW_DIR, "text-styles.json")) else []
effect_styles_raw = load("effect-styles.json")["effectStyles"] if os.path.exists(os.path.join(RAW_DIR, "effect-styles.json")) else []

final = {
    "file": {"name": overview.get("fileDisplayName", overview["fileName"]), "key": overview["fileKey"], "inspectedAt": overview.get("inspectedAt", "")},
    "collections": collections_out,
    "variables": final_vars,
    "textStyles": [{"name": s["name"], "fontFamily": s["fontFamily"], "fontStyle": s["fontStyle"],
                     "fontSize": s["fontSize"], "lineHeight": s["lineHeight"], "letterSpacing": s["letterSpacing"],
                     "textCase": s.get("textCase"), "textDecoration": s.get("textDecoration"),
                     "paragraphSpacing": s.get("paragraphSpacing"), "paragraphIndent": s.get("paragraphIndent"),
                     "leadingTrim": s.get("leadingTrim"),
                     "boundVariables": s["boundVariables"]} for s in text_styles_raw],
    "effectStyles": [{"name": s["name"], "effects": s["effects"]} for s in effect_styles_raw],
    "frames": frames_out,
}

out_path = os.path.join(OUT_DIR, "figma-variables.json")
with open(out_path, "w") as f:
    json.dump(final, f, indent=2, ensure_ascii=False)
print(f"\n[merge] wrote {out_path}  ({os.path.getsize(out_path)} bytes, {len(final_vars)} variables)")
