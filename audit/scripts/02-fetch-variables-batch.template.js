// Step 2 of 4. Read only. Run once PER BATCH, per collection.
//
// Fill in COLLECTION_ID, COLLECTION_NAME, MODES and a START/END slice range
// before each call, then paste the result to
// ../raw/<collection-slug>_<start>-<end>.json
//
// Why batches: the use_figma tool caps a single response at ~20KB. A
// collection with long descriptions (Component Tokens, Color Mode Switch,
// Raw Colors Values) needs small batches (12-20 variables); a collection
// with short/no descriptions (Screen Size Switch, Semantic Tokens) can go
// up to ~22-25 at a time. If a result comes back truncated ("// truncated
// to 20kb"), or if the returned `batchCount`/`variables.length` doesn't
// match what you asked for, HALVE the batch size and redo that range —
// don't just take what came back, or you'll silently drop variables (this
// happened during the original audit and was only caught by merge.py's
// count/alias verification).
//
// COLLECTION_ID and its modes come from 00-overview.json's
// collectionSummaries. Slice indices are into that same collection's
// variableIds array — pass them as plain numbers, never retype the id
// strings by hand.

const COLLECTION_ID = "VariableCollectionId:REPLACE_ME";
const COLLECTION_NAME = "REPLACE_ME";
const MODES = [{ modeId: "REPLACE_ME", name: "REPLACE_ME" }]; // from 00-overview.json
const START = 0, END = 20; // slice range into this collection's variableIds array

const collection = await figma.variables.getVariableCollectionByIdAsync(COLLECTION_ID);
const modes = MODES.length && MODES[0].modeId !== "REPLACE_ME" ? MODES : collection.modes;
const idsBatch = collection.variableIds.slice(START, END);
const vars = await Promise.all(idsBatch.map(id => figma.variables.getVariableByIdAsync(id)));

const aliasTargetIds = new Set();
for (const v of vars) {
  if (!v) continue;
  for (const modeId of Object.keys(v.valuesByMode)) {
    const val = v.valuesByMode[modeId];
    if (val && typeof val === "object" && val.type === "VARIABLE_ALIAS") aliasTargetIds.add(val.id);
  }
}
const aliasIdArr = [...aliasTargetIds];
const aliasTargets = await Promise.all(aliasIdArr.map(id => figma.variables.getVariableByIdAsync(id)));
const aliasById = new Map();
aliasIdArr.forEach((id, i) => aliasById.set(id, aliasTargets[i]));
const aliasCollectionIds = new Set();
for (const av of aliasTargets) if (av) aliasCollectionIds.add(av.variableCollectionId);
const aliasCollIdArr = [...aliasCollectionIds];
const aliasCollections = await Promise.all(aliasCollIdArr.map(id => figma.variables.getVariableCollectionByIdAsync(id)));
const aliasCollectionById = new Map();
aliasCollIdArr.forEach((id, i) => aliasCollectionById.set(id, aliasCollections[i]));

function toHex(rgba) {
  const toByte = (v) => Math.max(0, Math.min(255, Math.round(v * 255))).toString(16).padStart(2, "0");
  const r = toByte(rgba.r), g = toByte(rgba.g), b = toByte(rgba.b);
  const a = rgba.a === undefined ? 1 : rgba.a;
  return a < 1 ? `#${r}${g}${b}${toByte(a)}` : `#${r}${g}${b}`;
}

const results = vars.map(v => {
  if (!v) return { missing: true };
  const valuesByMode = {};
  for (const mode of modes) {
    const val = v.valuesByMode[mode.modeId];
    if (val === undefined) {
      valuesByMode[mode.name] = { missing: true };
    } else if (val && typeof val === "object" && val.type === "VARIABLE_ALIAS") {
      const target = aliasById.get(val.id);
      const targetCollection = target ? aliasCollectionById.get(target.variableCollectionId) : null;
      valuesByMode[mode.name] = {
        alias: target ? target.name : null,
        aliasCollection: targetCollection ? targetCollection.name : null,
        aliasId: val.id,
        broken: !target,
      };
    } else if (v.resolvedType === "COLOR" && val && typeof val === "object") {
      valuesByMode[mode.name] = { value: toHex(val) };
    } else {
      valuesByMode[mode.name] = { value: val };
    }
  }
  return {
    id: v.id, name: v.name, collection: COLLECTION_NAME, type: v.resolvedType,
    description: v.description || "", scopes: v.scopes || [], codeSyntax: v.codeSyntax || {},
    hiddenFromPublishing: v.hiddenFromPublishing || false, remote: v.remote || false, valuesByMode,
  };
});

return { collection: COLLECTION_NAME, start: START, end: END, batchCount: results.length, variables: results };
