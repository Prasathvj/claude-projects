// BIT: the robot sidekick rig. Three body styles share one face system on a visor screen.
// BIT.render({ style:'classic'|'orb'|'crt', state:'normal'|'scan'|'hijack'|'gasp'|'happy'|'worried', arms:'down'|'wave'|'type'|'stop'|'hug', extra:[], tilt, w, h })
(function (g) {
  const K = { shell: '#F3E6DC', shellS: '#D8C4B4', dark: '#160B06', accent: '#F87736', blue: '#55C2FF', red: '#FF3B30', ink: '#1A0A04' };
  const VIS = { normal: K.blue, scan: K.blue, happy: K.blue, gasp: K.blue, worried: K.blue, hijack: K.red };

  function face(cx, cy, s, state) {
    const c = VIS[state] ?? K.blue;
    const glow = `<ellipse cx="${cx}" cy="${cy}" rx="${70 * s}" ry="${34 * s}" fill="${c}" opacity=".18"/>`;
    const L = cx - 26 * s, R = cx + 26 * s;
    let eyes;
    switch (state) {
      case 'hijack': eyes = `<path d="M${L - 16 * s} ${cy - 10 * s} L${L + 14 * s} ${cy} L${L - 16 * s} ${cy + 8 * s} Z M${R + 16 * s} ${cy - 10 * s} L${R - 14 * s} ${cy} L${R + 16 * s} ${cy + 8 * s} Z" fill="${c}"/>`; break;
      case 'happy': eyes = `<path d="M${L - 13 * s} ${cy + 5 * s} Q${L} ${cy - 12 * s} ${L + 13 * s} ${cy + 5 * s} M${R - 13 * s} ${cy + 5 * s} Q${R} ${cy - 12 * s} ${R + 13 * s} ${cy + 5 * s}" stroke="${c}" stroke-width="${7 * s}" fill="none" stroke-linecap="round"/>`; break;
      case 'gasp': eyes = `<circle cx="${L}" cy="${cy}" r="${15 * s}" fill="none" stroke="${c}" stroke-width="${6 * s}"/><circle cx="${R}" cy="${cy}" r="${15 * s}" fill="none" stroke="${c}" stroke-width="${6 * s}"/><circle cx="${L}" cy="${cy}" r="${4 * s}" fill="${c}"/><circle cx="${R}" cy="${cy}" r="${4 * s}" fill="${c}"/>`; break;
      case 'worried': eyes = `<rect x="${L - 10 * s}" y="${cy - 12 * s}" width="${20 * s}" height="${24 * s}" rx="${10 * s}" fill="${c}"/><rect x="${R - 10 * s}" y="${cy - 12 * s}" width="${20 * s}" height="${24 * s}" rx="${10 * s}" fill="${c}"/><path d="M${L - 16 * s} ${cy - 22 * s} L${L + 12 * s} ${cy - 16 * s} M${R + 16 * s} ${cy - 22 * s} L${R - 12 * s} ${cy - 16 * s}" stroke="${c}" stroke-width="${5 * s}" stroke-linecap="round"/>`; break;
      case 'scan': eyes = `<rect x="${L - 12 * s}" y="${cy - 14 * s}" width="${24 * s}" height="${28 * s}" rx="${12 * s}" fill="${c}"/><rect x="${R - 12 * s}" y="${cy - 14 * s}" width="${24 * s}" height="${28 * s}" rx="${12 * s}" fill="${c}"/><rect x="${cx - 56 * s}" y="${cy + 1 * s}" width="${112 * s}" height="${3 * s}" fill="${c}" opacity=".8"/>`; break;
      default: eyes = `<rect x="${L - 12 * s}" y="${cy - 14 * s}" width="${24 * s}" height="${28 * s}" rx="${12 * s}" fill="${c}"/><rect x="${R - 12 * s}" y="${cy - 14 * s}" width="${24 * s}" height="${28 * s}" rx="${12 * s}" fill="${c}"/>`;
    }
    const mouth = state === 'gasp' ? `<ellipse cx="${cx}" cy="${cy + 26 * s}" rx="${7 * s}" ry="${9 * s}" fill="${c}"/>`
      : state === 'hijack' ? `<path d="M${cx - 16 * s} ${cy + 28 * s} h${8 * s} l${4 * s} ${-5 * s} l${4 * s} ${5 * s} l${4 * s} ${-5 * s} l${4 * s} ${5 * s} h${8 * s}" stroke="${c}" stroke-width="${4 * s}" fill="none"/>`
      : state === 'worried' ? `<path d="M${cx - 12 * s} ${cy + 28 * s} q${6 * s} ${-6 * s} ${12 * s} 0 t${12 * s} 0" stroke="${c}" stroke-width="${4 * s}" fill="none"/>`
      : `<path d="M${cx - 12 * s} ${cy + 24 * s} Q${cx} ${cy + 32 * s} ${cx + 12 * s} ${cy + 24 * s}" stroke="${c}" stroke-width="${4 * s}" fill="none" stroke-linecap="round"/>`;
    return glow + eyes + mouth;
  }

  function arms(pose, lx, rx, y, col) {
    const hand = (x, yy) => `<circle cx="${x}" cy="${yy}" r="13" fill="${col}"/>`;
    const seg = (d) => `<path d="${d}" stroke="${col}" stroke-width="12" fill="none" stroke-linecap="round"/>`;
    switch (pose) {
      case 'wave': return seg(`M${lx} ${y} q-26 14 -30 44`) + hand(lx - 30, y + 46) + seg(`M${rx} ${y} q30 -10 34 -56`) + hand(rx + 34, y - 60) + `<path d="M${rx + 52} ${y - 84} q8 8 2 18 M${rx + 62} ${y - 70} q8 8 2 18" stroke="${K.accent}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
      case 'type': return seg(`M${lx} ${y} q-10 30 18 46`) + hand(lx + 18, y + 46) + seg(`M${rx} ${y} q10 30 -18 46`) + hand(rx - 18, y + 46) + `<rect x="${lx - 10}" y="${y + 56}" width="${rx - lx + 20}" height="22" rx="6" fill="${K.dark}" stroke="${K.accent}" stroke-width="3"/>`;
      case 'stop': return seg(`M${lx} ${y} q-26 14 -30 44`) + hand(lx - 30, y + 46) + seg(`M${rx} ${y} q40 -4 56 -40`) + hand(rx + 56, y - 42);
      case 'hug': return seg(`M${lx} ${y} q30 20 50 4`) + hand(lx + 50, y + 4) + seg(`M${rx} ${y} q-30 20 -50 4`) + hand(rx - 50, y + 4);
      default: return seg(`M${lx} ${y} q-22 16 -24 44`) + hand(lx - 24, y + 46) + seg(`M${rx} ${y} q22 16 24 44`) + hand(rx + 24, y + 46);
    }
  }

  function stopSign(x, y) {
    return `<path d="M${x} ${y} V${y - 50}" stroke="#8A7A70" stroke-width="6" stroke-linecap="round"/><polygon points="${[...Array(8)].map((_, i) => { const a = Math.PI / 8 + i * Math.PI / 4; return `${x + Math.cos(a) * 34},${y - 84 + Math.sin(a) * 34}`; }).join(' ')}" fill="${K.red}" stroke="#fff" stroke-width="4"/><text x="${x}" y="${y - 77}" font-family="SD Display" font-weight="900" font-size="19" fill="#fff" text-anchor="middle">STOP</text>`;
  }

  function extras(list, top) {
    let s = '';
    for (const e of list) {
      if (e === 'sweat') s += `<path d="M276 ${top + 10} q12 22 0 30 q-12 -8 0 -30 Z" fill="${K.blue}"/>`;
      if (e === 'alert') s += `<text x="300" y="${top + 40}" font-family="SD Display" font-weight="900" font-size="64" fill="${K.red}">!</text>`;
      if (e === 'uhoh') s += `<rect x="230" y="${top - 46}" width="120" height="46" rx="14" fill="${K.dark}" stroke="${K.accent}" stroke-width="3"/><text x="290" y="${top - 15}" font-family="SD Display" font-weight="900" font-size="22" fill="${K.accent}" text-anchor="middle">uh-oh…</text>`;
      if (e === 'done') s += `<rect x="226" y="${top - 46}" width="160" height="46" rx="14" fill="${K.dark}" stroke="${K.blue}" stroke-width="3"/><text x="306" y="${top - 15}" font-family="SD Display" font-weight="900" font-size="20" fill="${K.blue}" text-anchor="middle">Task complete!</text>`;
      if (e === 'laser') s += `<path d="M200 ${top + 120} L60 ${top + 300} L340 ${top + 300} Z" fill="${K.blue}" opacity=".18"/>`;
    }
    return s;
  }

  function thruster(cx, y, t) {
    return `<ellipse cx="${cx}" cy="${y + 30}" rx="46" ry="10" fill="rgba(0,0,0,.4)"/><path d="M${cx - 16} ${y} Q${cx} ${y + 36} ${cx + 16} ${y} Z" fill="${K.accent}" opacity=".9"/><path d="M${cx - 8} ${y} Q${cx} ${y + 20} ${cx + 8} ${y} Z" fill="#FFE2CC"/>`;
  }

  function render(o = {}) {
    const st = o.style ?? 'classic', state = o.state ?? 'normal';
    const armCol = K.shellS;
    let body = '';
    if (st === 'classic') {
      body = thruster(200, 300) +
        `<rect x="120" y="196" width="160" height="110" rx="40" fill="${K.accent}"/><rect x="160" y="226" width="80" height="40" rx="12" fill="${K.dark}"/><circle cx="182" cy="246" r="6" fill="${VIS[state]}"/><circle cx="218" cy="246" r="6" fill="${K.accent}"/>` +
        arms(o.arms, 128, 272, 224, armCol) +
        `<path d="M200 54 V26" stroke="${K.shellS}" stroke-width="8"/><circle cx="200" cy="22" r="11" fill="${state === 'hijack' ? K.red : K.accent}"/>` +
        `<rect x="96" y="52" width="208" height="150" rx="56" fill="${K.shell}"/><rect x="96" y="52" width="208" height="150" rx="56" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="3"/>` +
        `<rect x="120" y="82" width="160" height="92" rx="34" fill="${K.dark}"/>` + face(200, 122, 1, state) +
        `<rect x="82" y="104" width="18" height="40" rx="8" fill="${K.shellS}"/><rect x="300" y="104" width="18" height="40" rx="8" fill="${K.shellS}"/>`;
    } else if (st === 'orb') {
      body = `<ellipse cx="200" cy="318" rx="60" ry="12" fill="rgba(0,0,0,.4)"/><ellipse cx="200" cy="290" rx="70" ry="12" fill="none" stroke="${K.accent}" stroke-width="6" opacity=".9"/>` +
        arms(o.arms, 96, 304, 176, K.accent) +
        `<circle cx="200" cy="170" r="112" fill="${K.shell}"/><path d="M88 170 A112 112 0 0 0 312 170 Z" fill="${K.shellS}" opacity=".45"/>` +
        `<rect x="104" y="118" width="192" height="92" rx="46" fill="${K.dark}"/>` + face(200, 158, 1, state) +
        `<circle cx="200" cy="58" r="9" fill="${state === 'hijack' ? K.red : K.accent}"/><path d="M180 66 Q200 50 220 66" stroke="${K.accent}" stroke-width="6" fill="none"/>`;
    } else {
      body = thruster(200, 312) +
        `<rect x="150" y="236" width="100" height="70" rx="12" fill="${K.shellS}"/><rect x="128" y="288" width="144" height="20" rx="8" fill="${K.shell}"/>` +
        arms(o.arms, 132, 268, 250, K.accent) +
        `<rect x="84" y="60" width="232" height="184" rx="28" fill="${K.shell}"/><rect x="84" y="60" width="232" height="184" rx="28" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="3"/>` +
        `<rect x="106" y="80" width="188" height="130" rx="20" fill="${K.dark}"/>` + face(200, 140, 1.05, state) +
        `<rect x="106" y="80" width="188" height="130" rx="20" fill="url(#scan)" opacity=".25"/><circle cx="290" cy="226" r="6" fill="${state === 'hijack' ? K.red : '#3DDC97'}"/><rect x="120" y="222" width="60" height="8" rx="4" fill="${K.shellS}"/>` +
        `<path d="M150 60 L130 26 M250 60 L270 26" stroke="${K.shellS}" stroke-width="6"/><circle cx="130" cy="24" r="8" fill="${K.accent}"/><circle cx="270" cy="24" r="8" fill="${K.accent}"/>`;
    }
    const defs = `<defs><pattern id="scan" width="4" height="6" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#fff"/></pattern></defs>`;
    return `<svg viewBox="0 0 400 360" width="${o.w ?? 400}" height="${o.h ?? 360}" style="overflow:visible">${defs}<g transform="rotate(${o.tilt ?? 0} 200 180)">${(o.extra || []).includes('laser') ? extras(['laser'], 40) : ''}${body}${o.arms === 'stop' ? stopSign(st === 'orb' ? 360 : st === 'crt' ? 324 : 328, st === 'orb' ? 134 : st === 'crt' ? 208 : 182) : ''}${extras((o.extra || []).filter((e) => e !== 'laser'), 40)}</g></svg>`;
  }
  g.BIT = { render, K };
})(typeof window !== 'undefined' ? window : globalThis);
