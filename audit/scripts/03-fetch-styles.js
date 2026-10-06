// Step 3 of 4. Read only. Two separate use_figma calls (or one after another).
// Save the first result as ../raw/text-styles.json and the second as
// ../raw/effect-styles.json.

// --- call A: text styles ---
{
  const textStyles = await figma.getLocalTextStylesAsync();
  const aliasTargetIds = new Set();
  for (const s of textStyles) {
    const bv = s.boundVariables || {};
    for (const key of Object.keys(bv)) { const e = bv[key]; if (e && e.id) aliasTargetIds.add(e.id); }
  }
  const aliasIdArr = [...aliasTargetIds];
  const aliasVars = await Promise.all(aliasIdArr.map(id => figma.variables.getVariableByIdAsync(id)));
  const aliasById = new Map();
  aliasIdArr.forEach((id, i) => aliasById.set(id, aliasVars[i]));

  const results = textStyles.map(s => {
    const bv = s.boundVariables || {};
    const boundVariables = {};
    for (const key of Object.keys(bv)) {
      const e = bv[key];
      const v = e && e.id ? aliasById.get(e.id) : null;
      boundVariables[key] = v ? v.name : (e ? e.id : null);
    }
    return {
      id: s.id, name: s.name,
      fontFamily: s.fontName ? s.fontName.family : null,
      fontStyle: s.fontName ? s.fontName.style : null,
      fontSize: s.fontSize, lineHeight: s.lineHeight, letterSpacing: s.letterSpacing,
      textCase: s.textCase, textDecoration: s.textDecoration,
      paragraphSpacing: s.paragraphSpacing, paragraphIndent: s.paragraphIndent, leadingTrim: s.leadingTrim,
      boundVariables,
    };
  });
  return { count: results.length, textStyles: results };
}

// --- call B: effect styles (run separately, comment out call A above first) ---
// const effectStyles = await figma.getLocalEffectStylesAsync();
// function toHex(rgba) {
//   const toByte = (v) => Math.max(0, Math.min(255, Math.round(v * 255))).toString(16).padStart(2, "0");
//   const r = toByte(rgba.r), g = toByte(rgba.g), b = toByte(rgba.b);
//   const a = rgba.a === undefined ? 1 : rgba.a;
//   return a < 1 ? `#${r}${g}${b}${toByte(a)}` : `#${r}${g}${b}`;
// }
// const aliasTargetIds = new Set();
// for (const s of effectStyles) for (const eff of s.effects) {
//   const bv = eff.boundVariables || {};
//   for (const key of Object.keys(bv)) { const e = bv[key]; if (e && e.id) aliasTargetIds.add(e.id); }
// }
// const aliasIdArr = [...aliasTargetIds];
// const aliasVars = await Promise.all(aliasIdArr.map(id => figma.variables.getVariableByIdAsync(id)));
// const aliasById = new Map();
// aliasIdArr.forEach((id, i) => aliasById.set(id, aliasVars[i]));
// const results = effectStyles.map(s => ({
//   id: s.id, name: s.name,
//   effects: s.effects.map(eff => {
//     const bv = eff.boundVariables || {};
//     const boundVariables = {};
//     for (const key of Object.keys(bv)) {
//       const e = bv[key];
//       const v = e && e.id ? aliasById.get(e.id) : null;
//       boundVariables[key] = v ? v.name : (e ? e.id : null);
//     }
//     return {
//       type: eff.type, radius: eff.radius ?? null, spread: eff.spread ?? null,
//       offset: eff.offset ? [eff.offset.x, eff.offset.y] : null,
//       color: eff.color ? toHex(eff.color) : null, visible: eff.visible,
//       blendMode: eff.blendMode || null, boundVariables,
//     };
//   }),
// }));
// return { count: results.length, effectStyles: results };
