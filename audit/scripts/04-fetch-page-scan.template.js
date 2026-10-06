// Step 4 of 4. Read only. Run ONCE PER PAGE — never loop pages inside one
// call (the figma-use skill's page rule). If there are N pages, fire N of
// these as separate use_figma calls in a single parallel batch. Save each
// result as ../raw/page-<page-name-lowercase-hyphenated>.json
//
// This also walks every node on the page to tally which local variables are
// bound to a layer (fills, strokes, spacing, sizing, text properties). It
// does NOT see variables bound to a component's own boolean/variant
// property, or per-character text overrides — note that limitation if you
// reuse boundNodeCount downstream. If a page is huge (the original audit's
// biggest page was ~4400 nodes and finished in well under a minute; if a
// page runs long, ~10 minutes, stop it, set boundVariableCounts to {} for
// that page, and say so rather than guessing).

const PAGE_ID = "REPLACE_ME";
const page = await figma.getNodeByIdAsync(PAGE_ID);
await figma.setCurrentPageAsync(page);

const topNodes = page.children.filter(n => ["FRAME", "COMPONENT", "COMPONENT_SET", "SECTION"].includes(n.type));
const frames = topNodes.map(n => ({ name: n.name, type: n.type, explicitVariableModes: n.explicitVariableModes || {} }));

const allNodes = page.findAll(() => true);
const counts = {};
function tally(boundVars) {
  if (!boundVars) return;
  for (const key of Object.keys(boundVars)) {
    const v = boundVars[key];
    if (Array.isArray(v)) {
      for (const entry of v) if (entry && entry.id) counts[entry.id] = (counts[entry.id] || 0) + 1;
    } else if (v && v.id) {
      counts[v.id] = (counts[v.id] || 0) + 1;
    }
  }
}
for (const n of allNodes) if ("boundVariables" in n && n.boundVariables) tally(n.boundVariables);

return {
  pageId: PAGE_ID, pageName: page.name, topNodeCount: page.children.length,
  frameCount: frames.length, frames, totalNodeCount: allNodes.length, boundVariableCounts: counts,
};
