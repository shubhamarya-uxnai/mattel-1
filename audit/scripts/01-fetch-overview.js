// Step 1 of 4. Read only.
//
// How to run: in a Claude session, load the `figma-use` skill, then call the
// `use_figma` tool with this file's contents as `code` and the file's key as
// `fileKey`. Save the JSON it returns as ../raw/00-overview.json.
//
// This lists every local variable collection (with its modes and variable
// count) and every page. It does NOT ignore "RunTime" itself here — do that
// filtering later, in merge.py — but nothing downstream will fetch RunTime's
// variables unless you ask it to.

const fileName = figma.root.name; // Figma's Plugin API only ever returns "Document" for
                                   // most files; it does not expose the human-facing file
                                   // title shown in the browser tab. Patch file.name by
                                   // hand afterwards in figma-variables.json if it matters.
const pages = figma.root.children.map(p => ({ id: p.id, name: p.name, type: p.type }));

const collections = await figma.variables.getLocalVariableCollectionsAsync();
const collectionSummaries = collections.map(c => ({
  id: c.id,
  name: c.name,
  hiddenFromPublishing: c.hiddenFromPublishing,
  defaultModeId: c.defaultModeId,
  modes: c.modes.map(m => ({ modeId: m.modeId, name: m.name })),
  variableCount: c.variableIds.length,
  variableIds: c.variableIds, // <- use these to plan your batch ranges for step 2
}));

return {
  fileName,
  fileKey: figma.fileKey || null,
  inspectedAt: new Date().toISOString().slice(0, 10),
  pageCount: pages.length,
  pages,
  collectionCount: collections.length,
  collectionSummaries,
};
