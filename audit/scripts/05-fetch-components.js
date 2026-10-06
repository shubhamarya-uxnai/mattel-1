// Step 5. Read only. Exports the six atom component sets on "Important Page"
// into raw JSON that merge-components.py assembles into ../components.json.
//
// Why two passes: a full recursive dump of every layer of every variant would
// be well over the ~20KB response cap for the 24-variant sets (Buttons,
// Icon-Buttons). So this is done in two kinds of call, both read-only:
//
//   PASS 1, full tree, ONE representative variant per set (6 calls, or fewer
//   if you batch small sets together). This is how you learn a set's SHAPE:
//   which layers exist, their auto-layout config, and which CSS-relevant
//   properties (fills, strokes, corner radius, padding, gap, font props) are
//   bound at all. Also dump any OTHER states/variants whose structure might
//   differ (Radio/Checkbox's Selected states add an inner dot or tick icon
//   that Default doesn't have; Input Field's Error/Disabled states change
//   which frames have a border). Use dumpFull() below.
//
//   PASS 2, compact bindings only, ALL variants of a set in one call. Once
//   you know the shape from pass 1, you don't need x/y/width/height or the
//   full tree again for every variant: code never hardcodes a pixel value
//   anyway, only the TOKEN each property is bound to matters. Walk the same
//   known layers by name and pull just their boundVariables. This is what
//   keeps 24-variant sets under the response cap in a single call. Use
//   extractCompactBindings() below, adjusted to the layer names your PASS 1
//   found (the ones here match this file's Buttons/Icon-Buttons/Chip).
//
// Save each result as ../raw-components/<NN>-<description>.json, in the
// numbering merge-components.py expects (see its file list), or update that
// script's file list if you rename anything.
//
// COMPONENT_SET_IDS below are this file's IDs; re-confirm the "Important
// Page" node ids if this is a different Figma file.

const COMPONENT_SET_IDS = {
  'Buttons': '21:86',
  'Icon-Buttons': '288:1521',
  'Chip': '28:88',
  'Input Field': '26:6135',
  'Radio Button': '29:146',
  'Checkbox': '26:9317',
};

// --- shared helpers, paste into every call below ---
function alias(v) {
  if (!v) return null;
  if (Array.isArray(v)) return alias(v[0]);
  return v.type === 'VARIABLE_ALIAS' ? v.id : null;
}

async function dumpFull(node) {
  const info = { name: node.name, type: node.type, visible: node.visible };
  if ('x' in node) info.x = node.x;
  if ('y' in node) info.y = node.y;
  if ('width' in node) info.width = node.width;
  if ('height' in node) info.height = node.height;
  if ('layoutMode' in node) info.layoutMode = node.layoutMode;
  if ('primaryAxisAlignItems' in node) info.primaryAxisAlignItems = node.primaryAxisAlignItems;
  if ('counterAxisAlignItems' in node) info.counterAxisAlignItems = node.counterAxisAlignItems;
  if ('itemSpacing' in node) info.itemSpacing = node.itemSpacing;
  if ('paddingLeft' in node) info.padding = [node.paddingLeft, node.paddingTop, node.paddingRight, node.paddingBottom];
  if ('layoutSizingHorizontal' in node) info.layoutSizingHorizontal = node.layoutSizingHorizontal;
  if ('layoutSizingVertical' in node) info.layoutSizingVertical = node.layoutSizingVertical;
  if ('layoutPositioning' in node) info.layoutPositioning = node.layoutPositioning;
  if ('cornerRadius' in node) info.cornerRadius = node.cornerRadius;
  if ('strokeAlign' in node) info.strokeAlign = node.strokeAlign;
  if ('strokeWeight' in node) info.strokeWeight = node.strokeWeight;
  if ('fills' in node && Array.isArray(node.fills)) info.fillsCount = node.fills.length;
  if ('strokes' in node && Array.isArray(node.strokes)) info.strokesCount = node.strokes.length;
  if ('characters' in node) info.characters = node.characters;
  if ('textStyleId' in node) info.textStyleId = node.textStyleId;
  if (node.boundVariables) {
    info.boundVariables = {};
    for (const [k, v] of Object.entries(node.boundVariables)) info.boundVariables[k] = alias(v);
  }
  if ('children' in node) info.children = await Promise.all(node.children.map((c) => dumpFull(c)));
  return info;
}

// --- PASS 1 example: one representative variant, full tree ---
// await figma.setCurrentPageAsync(figma.root.children.find(p => p.name === 'Important Page'));
// const set = await figma.getNodeByIdAsync(COMPONENT_SET_IDS['Buttons']);
// const variant = set.children.find(c => c.name === 'Size=Large, Type=Primary, Fill=On, Hover=Off');
// return { variantName: variant.name, variantId: variant.id, tree: await dumpFull(variant) };

// --- PASS 2 example: all variants of a set, compact bindings only ---
// Adjust the layer-finder lines (icon/text/ring) to match what PASS 1 showed
// for the set you're fetching; Buttons/Icon-Buttons/Chip all differ slightly.
//
// await figma.setCurrentPageAsync(figma.root.children.find(p => p.name === 'Important Page'));
// const set = await figma.getNodeByIdAsync(COMPONENT_SET_IDS['Buttons']);
// const out = [];
// for (const v of set.children) {
//   const bv = v.boundVariables || {};
//   const icon = v.children.find(c => c.type === 'INSTANCE' && c.visible);
//   const text = v.children.find(c => c.type === 'TEXT');
//   const ring = v.children.find(c => c.type === 'RECTANGLE');
//   out.push({
//     name: v.name,
//     root: { itemSpacing: alias(bv.itemSpacing), paddingH: alias(bv.paddingLeft), paddingV: alias(bv.paddingTop),
//       cornerRadius: alias(bv.topLeftRadius), borderWidth: alias(bv.strokeTopWeight),
//       fill: alias(bv.fills), border: alias(bv.strokes) },
//     icon: icon ? { name: icon.name, visible: icon.visible,
//       size: alias((icon.boundVariables||{}).width) || alias((icon.boundVariables||{}).height),
//       iconColor: icon.children && icon.children[0] ? alias((icon.children[0].boundVariables||{}).fills) : null } : null,
//     text: text ? { fill: alias((text.boundVariables||{}).fills), fontSize: alias((text.boundVariables||{}).fontSize),
//       fontFamily: alias((text.boundVariables||{}).fontFamily), fontWeight: alias((text.boundVariables||{}).fontWeight) } : null,
//     ring: ring ? { visible: ring.visible, x: ring.x, y: ring.y, width: ring.width, height: ring.height,
//       cornerRadius: alias((ring.boundVariables||{}).topLeftRadius), strokeWidth: alias((ring.boundVariables||{}).strokeTopWeight),
//       strokeAlign: ring.strokeAlign, stroke: alias((ring.boundVariables||{}).strokes) } : null,
//   });
// }
// return { count: out.length, variants: out };
//
// Input Field, Radio Button and Checkbox have nested Frames and multiple text
// layers rather than one icon+one text slot; for those, PASS 1's dumpFull()
// on every state (5 for Input Field, 3 each for Radio/Checkbox: small enough
// to fit the response cap even as full trees) is simpler than writing a
// bespoke compact extractor, and is what the 22 Sep run actually did.
