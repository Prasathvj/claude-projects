// HOST RIG: a 2D puppet of the channel's hoodie tech host, drawn as SVG from parameters so every
// expression, mouth shape (viseme) and arm pose is a value you can animate frame by frame.
// host(svgString) = HOST.render({ brows, eyes, mouth, arms, tilt, look, extra, blink }).
(function (g) {
  const C = { skin: '#E9B691', skinS: '#D69C77', hair: '#3A2418', hood: '#F87736', hoodS: '#D85E25', hoodIn: '#2A140C',
    ink: '#1A0A04', white: '#FFF7F0', glass: '#1A0A04', phone: '#2A1912', accent: '#F87736', blush: '#F28C7A' };


  function shade(hex, k) {
    const n = parseInt(hex.slice(1), 16); let r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    const f = (c) => Math.max(0, Math.min(255, Math.round(c + (k < 0 ? c * k : (255 - c) * k))));
    return '#' + [f(r), f(g), f(b)].map((c) => c.toString(16).padStart(2, '0')).join('');
  }
  const HAIR = {
    messy: (L) => `<path d="M126 168 C118 108 162 92 204 96 C252 100 284 126 274 172 C262 148 240 140 222 138 C210 152 170 160 150 150 C140 158 132 162 126 168 Z" fill="${L.hairCol}"/><path d="M180 100 q14 -26 32 -6 q10 -18 24 -4" stroke="${L.hairCol}" stroke-width="10" fill="none" stroke-linecap="round"/>`,
    fade: (L) => `<path d="M128 162 C124 112 160 98 200 98 C240 98 276 112 272 162 C266 140 246 128 200 128 C154 128 134 140 128 162 Z" fill="${L.hairCol}"/><path d="M128 162 C128 176 130 186 134 196 L140 196 C136 180 136 168 140 156 Z M272 162 C272 176 270 186 266 196 L260 196 C264 180 264 168 260 156 Z" fill="${L.hairCol}" opacity=".55"/>`,
    curly: (L) => { let c = ''; for (let i = 0; i <= 12; i++) { const a = Math.PI * (1.02 + i * 0.08); const x = 200 + Math.cos(a) * 74, y = 168 + Math.sin(a) * 70; c += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${22 + (i % 3) * 3}" fill="${L.hairCol}"/>`; } return c + `<circle cx="200" cy="104" r="34" fill="${L.hairCol}"/>`; },
    long: (L) => `<path d="M124 176 C118 108 164 92 204 94 C250 96 284 120 276 178 C262 140 236 126 206 124 C176 140 146 150 124 176 Z" fill="${L.hairCol}"/><path d="M206 124 C232 132 262 150 276 182 L276 150 C268 120 240 110 206 124 Z" fill="${shade(L.hairCol, 0.12)}"/>`,
    bun: (L) => `<circle cx="200" cy="90" r="28" fill="${L.hairCol}"/><path d="M126 168 C120 112 160 98 200 98 C240 98 280 112 274 168 C262 140 236 128 200 128 C164 128 138 140 126 168 Z" fill="${L.hairCol}"/>`,
    beanie: (L) => `<path d="M122 160 C118 98 160 82 200 82 C240 82 282 98 278 160 Z" fill="${L.hat}"/><rect x="118" y="140" width="164" height="30" rx="14" fill="${shade(L.hat, -0.2)}"/>${[0, 1, 2, 3, 4, 5, 6].map((i) => `<rect x="${128 + i * 22}" y="144" width="6" height="22" rx="3" fill="${shade(L.hat, -0.35)}"/>`).join('')}<circle cx="200" cy="80" r="14" fill="${shade(L.hat, -0.2)}"/>`,
    cap: (L) => `<path d="M124 162 C118 104 160 88 200 88 C240 88 282 104 276 162 Z" fill="${L.hat}"/><rect x="170" y="150" width="60" height="16" rx="6" fill="${shade(L.hat, -0.3)}"/><path d="M124 162 C150 154 250 154 276 162 L276 170 C250 162 150 162 124 170 Z" fill="${shade(L.hat, -0.2)}"/><circle cx="200" cy="96" r="7" fill="${shade(L.hat, -0.3)}"/><path d="M140 168 q10 -8 22 0 M238 168 q10 -8 22 0" stroke="${L.hairCol}" stroke-width="8" fill="none" stroke-linecap="round"/>`,
    buzz: (L) => `<path d="M130 160 C126 112 162 100 200 100 C238 100 274 112 270 160 C262 138 240 128 200 128 C160 128 138 138 130 160 Z" fill="${L.hairCol}" opacity=".85"/>`,
  };
  const GLASSES = {
    round: () => `<g fill="none" stroke="${C.glass}" stroke-width="6"><rect x="134" y="152" width="56" height="50" rx="18"/><rect x="210" y="152" width="56" height="50" rx="18"/><path d="M190 172 h20"/></g>`,
    square: () => `<g fill="none" stroke="${C.glass}" stroke-width="7"><rect x="132" y="154" width="60" height="46" rx="6"/><rect x="208" y="154" width="60" height="46" rx="6"/><path d="M192 172 h16"/></g>`,
    visor: () => `<rect x="126" y="156" width="148" height="44" rx="22" fill="${C.accent}" opacity=".92"/><rect x="140" y="164" width="44" height="8" rx="4" fill="#FFE2CC" opacity=".85"/>`,
    none: () => '',
  };
  const BEARD = {
    stubble: (L) => `<path d="M134 214 C140 262 170 276 200 276 C230 276 260 262 266 214 C254 248 232 258 200 258 C168 258 146 248 134 214 Z" fill="${L.hairCol}" opacity=".35"/>`,
    beard: (L) => `<path d="M130 200 C132 262 168 282 200 282 C232 282 268 262 270 200 C262 236 244 244 226 236 C214 230 186 230 174 236 C156 244 138 236 130 200 Z" fill="${L.hairCol}"/>`,
  };
  const PHONES = {
    neck: () => `<path d="M128 312 C128 286 152 278 168 290 M272 312 C272 286 248 278 232 290" stroke="#2B2B2B" stroke-width="12" fill="none" stroke-linecap="round"/><rect x="110" y="300" width="34" height="44" rx="14" fill="#2B2B2B"/><rect x="256" y="300" width="34" height="44" rx="14" fill="#2B2B2B"/><rect x="116" y="308" width="22" height="28" rx="9" fill="${C.accent}"/><rect x="262" y="308" width="22" height="28" rx="9" fill="${C.accent}"/>`,
    ears: () => `<path d="M124 196 C116 100 284 100 276 196" stroke="#2B2B2B" stroke-width="12" fill="none"/><rect x="108" y="172" width="30" height="52" rx="14" fill="#2B2B2B"/><rect x="262" y="172" width="30" height="52" rx="14" fill="#2B2B2B"/><rect x="113" y="180" width="20" height="36" rx="9" fill="${C.accent}"/><rect x="267" y="180" width="20" height="36" rx="9" fill="${C.accent}"/>`,
    headset: () => PHONES.ears() + `<path d="M124 214 C130 252 160 250 176 242" stroke="#2B2B2B" stroke-width="6" fill="none" stroke-linecap="round"/><circle cx="180" cy="241" r="7" fill="${C.accent}"/>`,
  };

  // ---- eyes: shapes per state; lx/ly = look direction (-1..1)
  function eye(cx, cy, kind, lx, ly, side, blink) {
    const px = cx + lx * 7, py = cy + ly * 5;
    if (blink >= 0.85 || kind === 'closed') return `<path d="M${cx - 15} ${cy + 2} Q${cx} ${cy + 8} ${cx + 15} ${cy + 2}" stroke="${C.ink}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
    if (kind === 'happy') return `<path d="M${cx - 15} ${cy + 5} Q${cx} ${cy - 12} ${cx + 15} ${cy + 5}" stroke="${C.ink}" stroke-width="5.5" fill="none" stroke-linecap="round"/>`;
    const ry = { open: 15, wide: 19, squint: 7, angry: 12, worried: 14 }[kind] ?? 15;
    const rx = kind === 'wide' ? 15 : 13;
    const pr = kind === 'wide' ? 5 : 7.5;
    let s = `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry * (1 - blink)}" fill="${C.white}"/>`;
    s += `<circle cx="${px}" cy="${py}" r="${pr}" fill="${C.ink}"/><circle cx="${px + 2.5}" cy="${py - 3}" r="2.2" fill="#fff"/>`;
    if (kind === 'angry') s += `<path d="M${cx - 17} ${cy - 16 + (side > 0 ? 8 : 0)} L${cx + 17} ${cy - 16 + (side > 0 ? 0 : 8)} L${cx + 17} ${cy - 24} L${cx - 17} ${cy - 24} Z" fill="${C.skin}"/>`;
    if (kind === 'squint') s += `<rect x="${cx - 16}" y="${cy - 20}" width="32" height="14" fill="${C.skin}"/>`;
    return s;
  }

  // ---- brows: [lift, angle] per expression
  const BROWS = { neutral: [0, 0], up: [-10, 0], high: [-16, 0], angry: [6, 18], worried: [-6, -16], skeptic: [0, 0, true], focused: [4, 6] };
  function brows(kind) {
    const [lift, ang, skeptic] = BROWS[kind] ?? [0, 0];
    const b = (cx, side) => {
      const a = skeptic ? (side < 0 ? -12 : 4) : ang * side;
      const l = skeptic ? (side < 0 ? -12 : 4) : lift;
      return `<rect x="${cx - 18}" y="${-6}" width="36" height="10" rx="5" fill="${C.brow}" transform="translate(0 ${145 + l}) rotate(${a} ${cx} 0)"/>`;
    };
    return b(162, -1) + b(238, 1);
  }

  // ---- mouths: expressions + visemes (A, E, O, M, F, rest)
  function mouth(kind) {
    const cx = 200, cy = 222;
    const M = {
      rest: `<path d="M${cx - 16} ${cy} Q${cx} ${cy + 6} ${cx + 16} ${cy}" stroke="${C.ink}" stroke-width="5" fill="none" stroke-linecap="round"/>`,
      smile: `<path d="M${cx - 26} ${cy - 4} Q${cx} ${cy + 18} ${cx + 26} ${cy - 4}" stroke="${C.ink}" stroke-width="5.5" fill="none" stroke-linecap="round"/>`,
      grin: `<path d="M${cx - 30} ${cy - 6} Q${cx} ${cy + 30} ${cx + 30} ${cy - 6} Z" fill="${C.ink}"/><path d="M${cx - 24} ${cy - 3} L${cx + 24} ${cy - 3} L${cx + 20} ${cy + 5} L${cx - 20} ${cy + 5} Z" fill="#fff"/><ellipse cx="${cx}" cy="${cy + 14}" rx="12" ry="5" fill="#E2685A"/>`,
      frown: `<path d="M${cx - 20} ${cy + 8} Q${cx} ${cy - 8} ${cx + 20} ${cy + 8}" stroke="${C.ink}" stroke-width="5.5" fill="none" stroke-linecap="round"/>`,
      flat: `<path d="M${cx - 18} ${cy + 2} L${cx + 18} ${cy + 2}" stroke="${C.ink}" stroke-width="5.5" stroke-linecap="round"/>`,
      smirk: `<path d="M${cx - 18} ${cy + 4} Q${cx + 4} ${cy + 8} ${cx + 22} ${cy - 8}" stroke="${C.ink}" stroke-width="5.5" fill="none" stroke-linecap="round"/>`,
      wavy: `<path d="M${cx - 22} ${cy + 2} q7 -7 11 0 t11 0 t11 0 t11 0" stroke="${C.ink}" stroke-width="5" fill="none" stroke-linecap="round"/>`,
      shock: `<ellipse cx="${cx}" cy="${cy + 8}" rx="16" ry="22" fill="${C.ink}"/><ellipse cx="${cx}" cy="${cy + 20}" rx="9" ry="6" fill="#E2685A"/>`,
      A: `<path d="M${cx - 20} ${cy - 2} Q${cx} ${cy - 6} ${cx + 20} ${cy - 2} Q${cx + 16} ${cy + 26} ${cx} ${cy + 26} Q${cx - 16} ${cy + 26} ${cx - 20} ${cy - 2} Z" fill="${C.ink}"/><ellipse cx="${cx}" cy="${cy + 18}" rx="9" ry="5" fill="#E2685A"/>`,
      E: `<path d="M${cx - 24} ${cy} Q${cx} ${cy - 4} ${cx + 24} ${cy} Q${cx} ${cy + 16} ${cx - 24} ${cy} Z" fill="${C.ink}"/><path d="M${cx - 18} ${cy} L${cx + 18} ${cy} L${cx + 15} ${cy + 4} L${cx - 15} ${cy + 4} Z" fill="#fff"/>`,
      O: `<ellipse cx="${cx}" cy="${cy + 6}" rx="12" ry="15" fill="${C.ink}"/>`,
      M: `<path d="M${cx - 18} ${cy + 3} L${cx + 18} ${cy + 3}" stroke="${C.ink}" stroke-width="7" stroke-linecap="round"/>`,
      F: `<path d="M${cx - 18} ${cy} Q${cx} ${cy + 10} ${cx + 18} ${cy} Z" fill="${C.ink}"/><rect x="${cx - 12}" y="${cy - 3}" width="24" height="6" rx="2" fill="#fff"/>`,
    };
    return M[kind] ?? M.rest;
  }

  // ---- arms (from shoulders at (120,330) and (280,330)); pose names
  function arm(pts, hand) {
    const d = 'M' + pts.map((p) => p.join(' ')).join(' L');
    return `<path d="${d}" stroke="${C.hood}" stroke-width="34" fill="none" stroke-linecap="round" stroke-linejoin="round"/>` +
      `<path d="${d}" stroke="${C.hoodS}" stroke-width="34" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".25" transform="translate(0 4)"/>` + hand;
  }
  const fist = (x, y, r = 17) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${C.skin}"/>`;
  const pointHand = (x, y, dir) => `<circle cx="${x}" cy="${y}" r="16" fill="${C.skin}"/><rect x="${dir > 0 ? x + 6 : x - 34}" y="${y - 6}" width="28" height="11" rx="5.5" fill="${C.skin}"/>`;
  const thumb = (x, y) => `<rect x="${x - 15}" y="${y - 12}" width="30" height="26" rx="10" fill="${C.skin}"/><rect x="${x - 6}" y="${y - 36}" width="12" height="28" rx="6" fill="${C.skin}"/>`;
  const palm = (x, y) => `<ellipse cx="${x}" cy="${y}" rx="17" ry="20" fill="${C.skin}"/><rect x="${x - 4}" y="${y - 36}" width="8" height="22" rx="4" fill="${C.skin}"/><rect x="${x - 15}" y="${y - 32}" width="8" height="20" rx="4" fill="${C.skin}"/><rect x="${x + 7}" y="${y - 32}" width="8" height="20" rx="4" fill="${C.skin}"/>`;
  function arms(pose) {
    const L = [120, 330], R = [280, 330];
    switch (pose) {
      case 'point': return arm([L, [96, 410], [118, 470]], fist(118, 476)) + arm([R, [352, 300], [400, 262]], pointHand(404, 258, 1));
      case 'shrug': return arm([L, [74, 380], [54, 316]], palm(54, 304)) + arm([R, [326, 380], [346, 316]], palm(346, 304));
      case 'chin': return arm([L, [96, 410], [118, 470]], fist(118, 476)) + arm([R, [300, 420], [236, 300]], fist(232, 270, 19));
      case 'facepalm': return arm([L, [96, 410], [118, 470]], fist(118, 476)) + arm([R, [300, 410], [222, 230]], palm(218, 176));
      case 'thumbs': return arm([L, [96, 410], [118, 470]], fist(118, 476)) + arm([R, [332, 400], [356, 330]], thumb(356, 330));
      case 'hands-up': return arm([L, [60, 300], [56, 220]], palm(56, 206)) + arm([R, [340, 300], [344, 220]], palm(344, 206));
      case 'phone': return arm([L, [110, 420], [170, 400]], '') + arm([R, [290, 420], [230, 400]], '') + `<rect x="160" y="352" width="80" height="60" rx="10" fill="${C.phone}" stroke="${C.accent}" stroke-width="4"/><circle cx="170" cy="400" r="16" fill="${C.skin}"/><circle cx="230" cy="400" r="16" fill="${C.skin}"/>`;
      default: return arm([L, [96, 410], [118, 470]], fist(118, 476)) + arm([R, [304, 410], [282, 470]], fist(282, 476));
    }
  }

  function extras(list) {
    let s = '';
    for (const e of list) {
      if (e === 'sweat') s += `<path d="M282 120 q12 22 0 30 q-12 -8 0 -30 Z" fill="#8FD3FF"/>`;
      if (e === 'blush') s += `<ellipse cx="146" cy="200" rx="16" ry="8" fill="${C.blush}" opacity=".55"/><ellipse cx="254" cy="200" rx="16" ry="8" fill="${C.blush}" opacity=".55"/>`;
      if (e === 'question') s += `<text x="300" y="70" font-family="SD Display" font-weight="900" font-size="72" fill="${C.accent}">?</text>`;
      if (e === 'bang') s += `<text x="292" y="74" font-family="SD Display" font-weight="900" font-size="78" fill="${C.accent}">!</text><text x="326" y="64" font-family="SD Display" font-weight="900" font-size="58" fill="${C.accent}">!</text>`;
      if (e === 'anger') s += `<g stroke="#E2453A" stroke-width="6" stroke-linecap="round"><path d="M276 70 l10 10 M296 70 l-10 10 M276 94 l10 -10 M296 94 l-10 -10"/></g>`;
      if (e === 'spark') s += `<g fill="${C.accent}"><path d="M320 80 l6 16 16 6 -16 6 -6 16 -6 -16 -16 -6 16 -6z"/><path d="M80 110 l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4z"/></g>`;
      if (e === 'glow') s += `<rect x="140" y="148" width="120" height="44" rx="20" fill="${C.accent}" opacity=".35"/>`;
    }
    return s;
  }

  function render(o = {}) {
    const L = Object.assign({ skin: '#E9B691', hair: 'messy', hairCol: '#3A2418', glasses: 'round', hood: 'up', top: '#F87736', topS: '#D85E25', inner: '#2A140C', strings: '#FFF7F0', phones: 'neck', beard: 'none', hat: '#F87736' }, o.char || {});
    const sk = L.skin, skS = shade(sk, -0.12);
    Object.assign(C, { brow: shade(L.hairCol, -0.5), skin: sk, skinS: skS, hair: L.hairCol, hood: L.top, hoodS: L.topS, hoodIn: L.inner });
    const tilt = o.tilt ?? 0, look = o.look ?? [0, 0], blink = o.blink ?? 0;
    const hoodUp = L.hood === 'up';
    const backHair = L.hair === 'long' ? `<path d="M116 186 C106 104 158 88 200 90 C242 88 294 104 284 186 L296 318 C276 332 254 324 248 304 L152 304 C146 324 124 332 104 318 Z" fill="${L.hairCol}"/>` : '';
    const hair = HAIR[L.hair] ? HAIR[L.hair](L) : HAIR.messy(L);
    const head = `
      <g transform="rotate(${tilt} 200 300)">
        ${hoodUp ? `<path d="M108 250 C96 140 140 70 200 70 C260 70 304 140 292 250 C282 300 248 320 200 320 C152 320 118 300 108 250 Z" fill="${C.hood}"/>
        <path d="M128 250 C120 160 156 100 200 100 C244 100 280 160 272 250 C262 290 236 306 200 306 C164 306 138 290 128 250 Z" fill="${C.hoodIn}"/>` : ''}
        ${backHair}
        <rect x="178" y="250" width="44" height="60" rx="16" fill="${C.skinS}"/>
        <ellipse cx="200" cy="190" rx="72" ry="82" fill="${C.skin}"/>
        <ellipse cx="128" cy="196" rx="12" ry="18" fill="${C.skinS}"/><ellipse cx="272" cy="196" rx="12" ry="18" fill="${C.skinS}"/>
        ${BEARD[L.beard] ? BEARD[L.beard](L) : ''}
        ${hair}
        ${brows(o.brows ?? 'neutral')}
        ${eye(162, 178, o.eyes ?? 'open', look[0], look[1], -1, blink)}
        ${eye(238, 178, o.eyes ?? 'open', look[0], look[1], 1, blink)}
        ${GLASSES[L.glasses] ? GLASSES[L.glasses](L) : ''}
        <path d="M196 198 q4 10 -4 14" stroke="${C.skinS}" stroke-width="5" fill="none" stroke-linecap="round"/>
        ${mouth(o.mouth ?? 'rest')}
        ${PHONES[L.phones] && L.phones !== 'neck' ? PHONES[L.phones](L) : ''}
        ${extras(o.extra ?? [])}
      </g>`;
    const body = `
      ${!hoodUp ? `<path d="M110 360 C100 300 150 290 200 300 C250 290 300 300 290 360 Z" fill="${C.hoodS}"/>` : ''}
      <path d="M70 520 C70 380 120 330 200 330 C280 330 330 380 330 520 Z" fill="${C.hood}"/>
      <path d="M150 336 C160 360 240 360 250 336" fill="${C.hoodS}"/>
      <path d="M182 350 L176 420 M218 350 L224 420" stroke="${L.strings}" stroke-width="6" stroke-linecap="round"/>
      <rect x="140" y="440" width="120" height="44" rx="14" fill="${C.hoodS}"/>
      ${L.phones === 'neck' ? PHONES.neck(L) : ''}`;
    return `<svg viewBox="0 0 400 520" width="${o.w ?? 400}" height="${o.h ?? 520}" style="overflow:visible">${body}${head}${arms(o.arms ?? 'down')}</svg>`;
  }

  g.HOST = { render, C, HAIR, GLASSES };
})(typeof window !== 'undefined' ? window : globalThis);
