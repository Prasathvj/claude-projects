// kodak01 scenes (RISE & FALL, Halftone Dossier). Spliced into index.html as the body of buildAll() by tools/build_dossier_kodak01.py.
  const K = __CUTS__;
  const head = (g, s, y = 300, max = 140, fill = C.ink, sh = C.orange) => {
    const sz = Math.min(max, 920 / measure(s, 100, F.slab, 400) * 100);
    return chars(g, s, { x: 80, y, size: sz, family: F.slab, weight: 400, fill, shadow: { fill: sh, dx: 8, dy: 8 } }); };
  const tag = (p, s, { size = 34, fill = C.ink, col = C.cream } = {}) => { const g = el('g', {}, p); const w = measure(s, size, F.mono, 800) + 40;
    el('rect', { x: -w / 2, y: -size * .9, width: w, height: size * 1.5, rx: 10, fill, stroke: C.ink, 'stroke-width': 5 }, g);
    txt(g, s, { x: 0, y: size * .2, 'font-size': size, 'font-family': F.mono, 'font-weight': 800, fill: col, 'text-anchor': 'middle' }); return g; };
  const drop = (t, t0, y1, d = .4) => lerp(2300, y1, E.back(seg(t, t0, t0 + d)));
  const xmark = (p, r = 120) => { const g = el('g', {}, p); const L = [];
    [[-1, -1, 1, 1], [1, -1, -1, 1]].forEach(([a, b, c, d]) => L.push(el('line', { x1: a * r, y1: b * r, x2: c * r, y2: d * r, stroke: C.red, 'stroke-width': 30, 'stroke-linecap': 'round', 'stroke-dasharray': r * 3, 'stroke-dashoffset': r * 3 }, g)));
    return { g, draw: (t, t0) => L.forEach((l, i) => l.setAttribute('stroke-dashoffset', (r * 3 * (1 - E.out(seg(t, t0 + i * .12, t0 + i * .12 + .15)))).toFixed(0))) }; };
  // the 1975 prototype: a boxy "toaster" with a lens, a cassette slot and dials
  const proto = (p) => { const g = el('g', { filter: 'url(#boil)' }, p);
    el('rect', { x: -240, y: -150, width: 480, height: 300, rx: 22, fill: '#D9CBB8', stroke: C.ink, 'stroke-width': 9 }, g);
    el('rect', { x: -240, y: -150, width: 480, height: 70, rx: 22, fill: '#9C8676', stroke: C.ink, 'stroke-width': 9 }, g);
    el('circle', { cx: -120, cy: 40, r: 88, fill: C.ink }, g); el('circle', { cx: -120, cy: 40, r: 58, fill: '#4A3E33', stroke: C.cream, 'stroke-width': 6 }, g);
    el('circle', { cx: -138, cy: 22, r: 14, fill: C.cream }, g);
    el('rect', { x: 20, y: -40, width: 190, height: 70, rx: 8, fill: C.ink }, g); el('rect', { x: 34, y: -28, width: 162, height: 18, rx: 4, fill: '#9C8676' }, g);
    [60, 120, 180].forEach(x => el('circle', { cx: x, cy: 90, r: 20, fill: C.orange, stroke: C.ink, 'stroke-width': 6 }, g));
    el('rect', { x: 160, y: -200, width: 40, height: 52, rx: 8, fill: C.red, stroke: C.ink, 'stroke-width': 6 }, g);
    txt(g, 'PROTOTYPE · 1975', { x: 0, y: -103, 'font-size': 30, 'font-family': F.mono, 'font-weight': 800, fill: C.cream, 'text-anchor': 'middle' }); return g; };
  const phone = (p, s = 1) => { const g = el('g', { filter: 'url(#boil)' }, p);
    el('rect', { x: -100 * s, y: -200 * s, width: 200 * s, height: 400 * s, rx: 34 * s, fill: C.ink, stroke: C.ink, 'stroke-width': 7 }, g);
    el('rect', { x: -84 * s, y: -172 * s, width: 168 * s, height: 330 * s, rx: 16 * s, fill: C.cream }, g);
    el('circle', { cx: 0, cy: -40 * s, r: 46 * s, fill: C.orange, stroke: C.ink, 'stroke-width': 6 }, g); el('circle', { cx: 0, cy: -40 * s, r: 20 * s, fill: C.ink }, g);
    el('rect', { x: -40 * s, y: 70 * s, width: 80 * s, height: 30 * s, rx: 15 * s, fill: C.red }, g); return g; };
  const reelG = (p, x) => { const g = el('g', {}, p); el('circle', { cx: 0, cy: 0, r: 52, fill: C.cream, stroke: C.ink, 'stroke-width': 7 }, g);
    for (let k = 0; k < 6; k++) el('rect', { x: -6, y: -46, width: 12, height: 22, rx: 3, fill: C.ink, transform: `rotate(${k * 60})` }, g); el('circle', { r: 14, fill: C.ink }, g); return g; };
  const cassette = (p) => { const g = el('g', { filter: 'url(#boil)' }, p);
    el('rect', { x: -260, y: -160, width: 520, height: 320, rx: 26, fill: C.ink, stroke: C.ink, 'stroke-width': 8 }, g);
    el('rect', { x: -220, y: -130, width: 440, height: 160, rx: 14, fill: C.yellow, stroke: C.ink, 'stroke-width': 6 }, g);
    txt(g, 'PHOTO_001', { x: 0, y: -88, 'font-size': 34, 'font-family': F.mono, 'font-weight': 800, fill: C.ink, 'text-anchor': 'middle' });
    el('rect', { x: -150, y: -60, width: 300, height: 80, rx: 40, fill: C.cream, stroke: C.ink, 'stroke-width': 6 }, g);
    el('path', { d: 'M-150 160 L-110 80 L110 80 L150 160 Z', fill: '#4A3E33' }, g);
    const r1 = reelG(g), r2 = reelG(g); tf(r1, -100, -20); tf(r2, 100, -20); return { g, r1, r2 }; };
  const toaster = (p) => { const g = el('g', { filter: 'url(#boil)' }, p);
    el('rect', { x: -200, y: -130, width: 400, height: 260, rx: 70, fill: C.yellow, stroke: C.ink, 'stroke-width': 9 }, g);
    [-70, 70].forEach(x => el('rect', { x: x - 55, y: -130, width: 110, height: 22, rx: 11, fill: C.ink }, g));
    el('rect', { x: 196, y: -40, width: 40, height: 22, rx: 8, fill: C.ink }, g);
    el('rect', { x: -150, y: 130, width: 60, height: 26, rx: 8, fill: C.ink }, g); el('rect', { x: 90, y: 130, width: 60, height: 26, rx: 8, fill: C.ink }, g);
    const cap = el('g', {}, g); el('path', { d: 'M-170 -190 L0 -250 L170 -190 L0 -130 Z', fill: C.ink, stroke: C.ink, 'stroke-width': 6, 'stroke-linejoin': 'round' }, cap);
    el('rect', { x: -80, y: -175, width: 160, height: 50, fill: C.ink }, cap);
    el('path', { d: 'M0 -190 L120 -170 L130 -90', fill: 'none', stroke: C.orange, 'stroke-width': 8 }, cap); el('circle', { cx: 130, cy: -82, r: 14, fill: C.orange }, cap);
    return { g, cap }; };
  const exec = (p) => { const g = el('g', {}, p); el('circle', { cx: 0, cy: -150, r: 70, fill: C.ink }, g);
    el('path', { d: 'M-130 60 C-130 -40 -80 -70 0 -70 C80 -70 130 -40 130 60 Z', fill: C.ink }, g);
    el('path', { d: 'M-14 -66 L14 -66 L8 20 L0 34 L-8 20 Z', fill: C.red }, g); return g; };
  const bubble = (p, s, size = 60, tailX = -80) => { const g = el('g', { filter: 'url(#boil)' }, p); const w = measure(s, size, F.slab, 400) + 80, h = size * 1.9;
    el('path', { d: `M${tailX - 30} ${h / 2 - 6} L${tailX + 10} ${h / 2 + 60} L${tailX + 40} ${h / 2 - 6} Z`, fill: C.cream, stroke: C.ink, 'stroke-width': 7, 'stroke-linejoin': 'round' }, g);
    el('rect', { x: -w / 2, y: -h / 2, width: w, height: h, rx: 40, fill: C.cream, stroke: C.ink, 'stroke-width': 8 }, g);
    el('rect', { x: tailX - 24, y: h / 2 - 14, width: 58, height: 16, fill: C.cream }, g);
    txt(g, s, { x: 0, y: size * .34, 'font-size': size, 'font-family': F.slab, fill: C.ink, 'text-anchor': 'middle' }); return g; };
  const filmRoll = (p) => { const g = el('g', { filter: 'url(#boil)' }, p);
    el('path', { d: 'M60 -40 L520 -40 L520 140 L60 140 Z', fill: '#4A3E33', stroke: C.ink, 'stroke-width': 7 }, g);
    for (let k = 0; k < 9; k++) { el('rect', { x: 80 + k * 50, y: -28, width: 26, height: 20, rx: 4, fill: C.cream }, g); el('rect', { x: 80 + k * 50, y: 108, width: 26, height: 20, rx: 4, fill: C.cream }, g); }
    for (let k = 0; k < 3; k++) el('rect', { x: 100 + k * 140, y: 2, width: 120, height: 96, rx: 6, fill: C.peach }, g);
    el('rect', { x: -170, y: -190, width: 240, height: 380, rx: 30, fill: C.orange, stroke: C.ink, 'stroke-width': 9 }, g);
    el('rect', { x: -190, y: -220, width: 280, height: 50, rx: 12, fill: C.ink }, g); el('rect', { x: -190, y: 170, width: 280, height: 50, rx: 12, fill: C.ink }, g);
    el('rect', { x: -150, y: -60, width: 200, height: 120, rx: 10, fill: C.yellow, stroke: C.ink, 'stroke-width': 6 }, g);
    txt(g, 'FILM', { x: -50, y: 22, 'font-size': 64, 'font-family': F.bagel, fill: C.ink, 'text-anchor': 'middle' }); return g; };
  const bill = (p) => { const b = el('g', { filter: 'url(#boil)' }, p); el('rect', { x: -70, y: -36, width: 140, height: 72, rx: 8, fill: '#8CCB8F', stroke: C.ink, 'stroke-width': 5 }, b);
    txt(b, '$', { x: 0, y: 18, 'font-size': 52, 'font-family': F.bagel, fill: C.ink, 'text-anchor': 'middle' }); return b; };
  const folder = (p, label) => { const g = el('g', { filter: 'url(#boil)' }, p);
    el('path', { d: 'M-260 -170 L-80 -170 L-50 -210 L120 -210 L150 -170 L260 -170 L260 190 L-260 190 Z', fill: C.peach, stroke: C.ink, 'stroke-width': 9, 'stroke-linejoin': 'round' }, g);
    el('rect', { x: -230, y: -120, width: 460, height: 280, rx: 6, fill: '#F2B98F', stroke: C.ink, 'stroke-width': 5 }, g);
    const lab = el('g', {}, g); el('rect', { x: -190, y: -40, width: 380, height: 90, rx: 8, fill: C.cream, stroke: C.ink, 'stroke-width': 6 }, lab);
    txt(lab, label, { x: 0, y: 22, 'font-size': Math.min(52, 330 / (Math.max(label.length, 1) * .6)), 'font-family': F.mono, 'font-weight': 800, fill: C.ink, 'text-anchor': 'middle' }); return { g }; };

  // ---------- S1  KODAK INVENTED THE DIGITAL CAMERA ----------
  scene(0, K.bur, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.yellow, step: 22, angle: 15, f: radial(560, 820, 760, 1.0), maxK: .66 });
    halftone(g, { color: C.orange, step: 20, angle: 60, f: edge(1100, 1.4), maxK: .6 }).setAttribute('class', 'mul');
    const h = head(g, 'INVENTED IT', 330);
    const cam = proto(g);
    const plate = el('g', {}, g); el('rect', { x: -330, y: -70, width: 660, height: 140, rx: 10, fill: C.ink }, plate);
    txt(plate, 'EASTMAN KODAK', { x: 0, y: 18, 'font-size': 66, 'font-family': F.slab, fill: C.cream, 'text-anchor': 'middle' });
    txt(plate, 'FILM & CAMERAS · ROCHESTER, NY', { x: 0, y: 56, 'font-size': 24, 'font-family': F.mono, 'font-weight': 800, fill: C.yellow, 'text-anchor': 'middle' });
    const dc = tag(g, 'THE DIGITAL CAMERA', { size: 40, fill: C.orange });
    return (t) => {
      tf(plate, 540, drop(t, 0.05, 520, .35), 1, -2);
      charsPop(h, t, Wt('invented') - .1, .045);
      tf(cam, 540, drop(t, Wt('digital') - .25, 930), 1.15, 2 * Math.sin(t * 3));
      tf(dc, 540, drop(t, Wt('camera') - .1, 1160), 1, -2);
    };
  });
  // ---------- S2  ...THEN BURIED IT. WHY? (dark) ----------
  scene(K.bur, K.c1, (g) => {
    bg(g, C.ink);
    halftone(g, { color: '#4A3E33', step: 22, angle: 30, f: radial(540, 900, 900, .9), maxK: .66 });
    const h = chars(g, 'THEN...', { x: 80, y: 340, size: 150, family: F.slab, weight: 400, fill: C.cream, shadow: { fill: C.red, dx: 9, dy: 9 } });
    const cam = proto(g);
    const dirt = el('g', { filter: 'url(#boil)' }, g); el('path', { d: 'M-520 120 C-380 -60 -200 -90 0 -100 C200 -90 380 -60 520 120 L520 520 L-520 520 Z', fill: '#6B4A33', stroke: C.cream, 'stroke-width': 7 }, dirt);
    const rr = rng(5); for (let k = 0; k < 26; k++) el('circle', { cx: (rr() - .5) * 900, cy: 40 + rr() * 300, r: 6 + rr() * 12, fill: '#4A3324' }, dirt);
    const st = stampEl(g, 'BURIED', { size: 140, color: C.red });
    const q = chars(g, '?', { x: 880, y: 900, size: 340, family: F.bagel, weight: 400, fill: C.red, anchor: 'middle', shadow: { fill: C.cream, dx: 10, dy: 10 } });
    return (t) => {
      charsPop(h, t, Wt('then') - .1, .05, .3, 50);
      tf(cam, 540, lerp(820, 1080, E.in(seg(t, Wt('buried') - .1, Wt('buried') + .5))), 1.05);
      tf(dirt, 540, lerp(1600, 1060, E.out(seg(t, Wt('buried') - .15, Wt('buried') + .3))));
      stampAnim(st, t, Wt('buried') + .1, 460, 560, -9);
      charsPop(q, t, Wt('why') - .05, .05, .35, 120);
    };
  });
  // ---------- S3  IT'S 1975 (calendar years flip) ----------
  scene(K.c1, K.eng, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.teal, step: 22, angle: 15, f: radial(540, 880, 720, 1.0), maxK: .64 }).setAttribute('class', 'mul');
    halftone(g, { color: C.yellow, step: 20, angle: 60, f: edge(1000, 1.5), maxK: .6 }).setAttribute('class', 'mul');
    const h = head(g, "IT'S 1975", 330);
    const cal = el('g', { filter: 'url(#boil)' }, g);
    const page = (parent, yr, col) => { const p = el('g', {}, parent);
      el('rect', { x: -320, y: -330, width: 640, height: 640, rx: 26, fill: C.cream, stroke: C.ink, 'stroke-width': 9 }, p);
      el('rect', { x: -320, y: -330, width: 640, height: 150, rx: 26, fill: col, stroke: C.ink, 'stroke-width': 9 }, p);
      txt(p, 'KODAK LAB', { x: 0, y: -232, 'font-size': 74, 'font-family': F.slab, fill: C.cream, 'text-anchor': 'middle' });
      txt(p, yr, { x: 0, y: 130, 'font-size': 240, 'font-family': F.bagel, fill: C.ink, 'text-anchor': 'middle' }); return p; };
    page(cal, '1975', C.red);
    const torn = ['1974', '1973', '1972'].map(y => page(cal, y, '#9C8676'));
    el('circle', { cx: 0, cy: -350, r: 26, fill: C.red, stroke: C.ink, 'stroke-width': 6 }, cal);
    return (t) => {
      charsPop(h, t, K.c1 + .05, .05);
      tf(cal, 540, lerp(-700, 880, E.out(seg(t, K.c1, K.c1 + .35))), .95);
      torn.forEach((p, i) => { const t0 = Wt('1975') - .1 + i * .14, q = seg(t, t0, t0 + .4);
        op(p, 1 - q); tf(p, lerp(0, (i - 1) * 420, E.in(q)), lerp(0, -900, E.in(q)), 1, lerp(0, (i - 1) * 40, q)); });
    };
  });
  // ---------- S4  A KODAK ENGINEER, STEVE SASSON, BUILDS THE WORLD'S FIRST PORTABLE DIGITAL CAMERA ----------
  scene(K.eng, K.c2, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.yellow, step: 22, angle: 15, f: radial(320, 760, 620, 1.0), maxK: .62 }).setAttribute('class', 'mul');
    const h = head(g, 'THE INVENTOR', 300);
    const badge = el('g', { filter: 'url(#boil)' }, g);
    el('path', { d: 'M-60 -420 L0 -250 L60 -420', fill: 'none', stroke: C.red, 'stroke-width': 16 }, badge);
    el('rect', { x: -220, y: -260, width: 440, height: 560, rx: 24, fill: C.cream, stroke: C.ink, 'stroke-width': 9 }, badge);
    el('rect', { x: -220, y: -260, width: 440, height: 90, rx: 24, fill: C.ink }, badge);
    txt(badge, 'KODAK · STAFF', { x: 0, y: -200, 'font-size': 36, 'font-family': F.mono, 'font-weight': 800, fill: C.yellow, 'text-anchor': 'middle' });
    el('rect', { x: -110, y: -150, width: 220, height: 230, rx: 14, fill: C.peach, stroke: C.ink, 'stroke-width': 6 }, badge);
    el('circle', { cx: 0, cy: -70, r: 52, fill: C.ink }, badge); el('path', { d: 'M-90 80 C-90 0 -50 -14 0 -14 C50 -14 90 0 90 80 Z', fill: C.ink }, badge);
    const nm = txt(badge, 'STEVE SASSON', { x: 0, y: 150, 'font-size': 52, 'font-family': F.slab, fill: C.ink, 'text-anchor': 'middle' });
    const role = txt(badge, 'ENGINEER', { x: 0, y: 210, 'font-size': 36, 'font-family': F.mono, 'font-weight': 800, fill: C.red, 'text-anchor': 'middle' });
    const cam = proto(g);
    const st = stampEl(g, "WORLD'S FIRST", { size: 96, color: C.red });
    const pc = tag(g, 'PORTABLE · SELF-CONTAINED', { size: 34, fill: C.orange });
    return (t) => {
      charsPop(h, t, K.eng + .05, .04);
      tf(badge, 290, drop(t, K.eng + .05, 700), .95, -3);
      op(nm, t > Wt('steve') - .05 ? 1 : 0); op(role, t > Wt('engineer') - .05 ? 1 : 0);
      tf(cam, 790, drop(t, Wt('builds') - .1, 700), .72, 4);
      stampAnim(st, t, Wt('first') + .05, 560, 1090, -6);
      tf(pc, 540, drop(t, Wt('portable') - .1, 1235, .3), 1, -2);
    };
  });
  // ---------- S5  LESS LIKE AN iPHONE, MORE LIKE A TOASTER THAT WENT TO ENGINEERING COLLEGE ----------
  scene(K.c2, K.c3, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.orange, step: 22, angle: 15, f: edge(1000, 1.3), maxK: .6 }).setAttribute('class', 'mul');
    halftone(g, { color: C.yellow, step: 24, angle: 60, f: radial(760, 860, 520, 1.0), maxK: .6 }).setAttribute('class', 'mul');
    const h = head(g, 'LOOKS LIKE...', 300);
    const ph = phone(g, 1.1); const lp = tag(g, 'A PHONE?', { size: 40 }); const x = xmark(g, 150);
    const ts = toaster(g); const lt = tag(g, 'A TOASTER', { size: 40, fill: C.orange });
    const grad = txt(g, 'class of 1975', { x: 0, y: 0, 'font-size': 40, 'font-family': F.mono, 'font-weight': 800, fill: C.red, 'text-anchor': 'middle' });
    return (t) => {
      charsPop(h, t, Wt('looks') - .1, .05);
      tf(ph, 270, drop(t, Wt('iphone') - .35, 800), 1, -5); tf(lp, 270, drop(t, Wt('iphone') - .2, 1110, .3));
      x.draw(t, Wt('and') - .05); tf(x.g, 270, 800);
      tf(ts.g, 760, drop(t, Wt('toaster') - .25, 860), .95, 3);
      tf(ts.cap, 0, lerp(-500, 0, E.back(seg(t, Wt('college') - .3, Wt('college')))), 1, lerp(-30, 0, seg(t, Wt('college') - .3, Wt('college'))));
      op(ts.cap, t > Wt('college') - .3 ? 1 : 0);
      tf(lt, 760, drop(t, Wt('toaster'), 1110, .3)); op(grad, t > Wt('college') ? 1 : 0); tf(grad, 760, 1190, 1, -3);
    };
  });
  // ---------- S6  SPECS: 3.6 KG, 16 BATTERIES, 0.01 MEGAPIXELS ----------
  scene(K.c3, K.c4, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.teal, step: 22, angle: 15, f: ramp(300, 1500), maxK: .58 }).setAttribute('class', 'mul');
    const h = head(g, 'THE SPECS', 300);
    const card = el('g', { filter: 'url(#boil)' }, g); el('rect', { x: -440, y: -420, width: 880, height: 840, rx: 18, fill: C.cream, stroke: C.ink, 'stroke-width': 9 }, card);
    txt(card, 'EXHIBIT 02 · SPEC SHEET', { x: -400, y: -350, 'font-size': 30, 'font-family': F.mono, 'font-weight': 800, fill: '#9C8676' });
    const rows = [['WEIGHT', '3.6 kg', '36'], ['POWER', '16 x AA', '16'], ['IMAGE', '0.01 MP', 'zero']].map(([k, v, w], i) => { const r = el('g', {}, card);
      txt(r, k, { x: -400, y: -230 + i * 170, 'font-size': 40, 'font-family': F.mono, 'font-weight': 800, fill: C.ink });
      const vt = txt(r, v, { x: 400, y: -215 + i * 170, 'font-size': 92, 'font-family': F.bagel, fill: i === 2 ? C.red : C.ink, 'text-anchor': 'end' });
      el('line', { x1: -400, x2: 400, y1: -170 + i * 170, y2: -170 + i * 170, stroke: '#D9C9B8', 'stroke-width': 4 }, r); return { r, w }; });
    const bats = el('g', {}, card); const B = [];
    for (let k = 0; k < 16; k++) { const b = el('g', {}, bats); el('rect', { x: -14, y: -34, width: 28, height: 68, rx: 6, fill: k % 2 ? C.orange : C.yellow, stroke: C.ink, 'stroke-width': 4 }, b); el('rect', { x: -6, y: -42, width: 12, height: 9, fill: C.ink }, b); tf(b, -380 + k * 50, 300); B.push(b); }
    const grid = el('g', {}, card); for (let k = 0; k < 100; k++) el('rect', { x: (k % 10) * 18, y: Math.floor(k / 10) * 18, width: 16, height: 16, fill: ['#6B5A4A', '#9C8676', '#D9CBB8', '#4A3E33'][(k * 7 + Math.floor(k / 10) * 3) % 4] }, grid);
    const st = stampEl(g, 'SHOCKING', { size: 86, color: C.red });
    return (t) => {
      charsPop(h, t, K.c3 + .05, .05);
      tf(card, 540, drop(t, K.c3 + .02, 840), 1, -1.5);
      rows.forEach(({ r, w }) => { const t0 = Wt(w) - .15; op(r, t > t0 ? 1 : 0); tf(r, lerp(-300, 0, E.out(seg(t, t0, t0 + .3))), 0); });
      B.forEach((b, k) => op(b, t > Wt('16') + k * .04 ? 1 : 0));
      op(grid, t > Wt('megapixels') - .1 ? 1 : 0); tf(grid, -380, 230, lerp(.4, 1, E.back(seg(t, Wt('megapixels') - .1, Wt('megapixels') + .2))));
      op(bats, t < Wt('megapixels') - .1 ? 1 : 0);
      stampAnim(st, t, Wt('shocking') + .05, 700, 1150, -8);
    };
  });
  // ---------- S7  23 SECONDS PER PHOTO, ON A CASSETTE TAPE ----------
  scene(K.c4, K.c5, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.yellow, step: 22, angle: 15, f: radial(540, 760, 700, 1.0), maxK: .62 }).setAttribute('class', 'mul');
    const h = head(g, 'ONE PHOTO =', 300);
    const cs = cassette(g);
    const tm = el('g', {}, g); const tmS = txt(tm, '0 SEC', { x: 8, y: 8, 'font-size': 150, 'font-family': F.bagel, fill: C.orange, class: 'mul', 'text-anchor': 'middle' }); const tmT = txt(tm, '0 SEC', { x: 0, y: 0, 'font-size': 150, 'font-family': F.bagel, fill: C.ink, 'text-anchor': 'middle' });
    const barBg = el('rect', { x: -330, y: 0, width: 660, height: 40, rx: 12, fill: C.cream, stroke: C.ink, 'stroke-width': 6 }, g);
    const bar = el('rect', { x: -330, y: 0, width: 0, height: 40, rx: 12, fill: C.orange, stroke: C.ink, 'stroke-width': 6 }, g);
    const lab = txt(g, 'SAVING TO TAPE...', { x: 0, y: 0, 'font-size': 34, 'font-family': F.mono, 'font-weight': 800, fill: C.ink, 'text-anchor': 'middle' });
    const st = stampEl(g, 'YES. A CASSETTE.', { size: 74, color: C.red });
    return (t) => {
      charsPop(h, t, K.c4 + .05, .05);
      tf(cs.g, 540, drop(t, K.c4 + .05, 740), 1.2, -2);
      const run = seg(t, Wt('takes'), Wt('tape') + .3);
      tf(cs.r1, -100, -20, 1, t * 260); tf(cs.r2, 100, -20, 1, t * 260);
      const v = Math.round(23 * E.out(seg(t, Wt('23') - .2, Wt('seconds') + .2))), s = v + ' SEC'; tmS.textContent = s; tmT.textContent = s;
      op(tm, t > Wt('23') - .25 ? 1 : 0); tf(tm, 540, 1080, t > Wt('seconds') ? lerp(1.3, 1, E.back(seg(t, Wt('seconds'), Wt('seconds') + .3))) : 1);
      tf(barBg, 540, 1130); tf(bar, 540, 1130); bar.setAttribute('width', (660 * run).toFixed(0)); tf(lab, 540, 1220); [barBg, bar, lab].forEach(e => op(e, t > Wt('takes') ? 1 : 0));
      stampAnim(st, t, Wt('yes') + .05, 560, 455, -5);
    };
  });
  // ---------- S8  THE MEETING: "THAT'S CUTE. BUT DON'T TELL ANYONE." (reported) ----------
  scene(K.c5, K.c6, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.orange, step: 22, angle: 30, f: edge(1000, 1.3), maxK: .62 }).setAttribute('class', 'mul');
    const h = head(g, 'THE BOSSES', 300);
    const rep = tag(g, 'REPORTED REACTION · NYT, 2008', { size: 30, fill: C.ink, col: C.yellow });
    const ex = [0, 1, 2].map(() => exec(g));
    const table = el('g', { filter: 'url(#boil)' }, g); el('rect', { x: -470, y: -40, width: 940, height: 80, rx: 14, fill: '#9C8676', stroke: C.ink, 'stroke-width': 8 }, table);
    const cam = proto(g);
    const b1 = bubble(g, "That's cute.", 64, -60), b2 = bubble(g, "But don't tell anyone.", 54, 120);
    const st = stampEl(g, 'CONFIDENTIAL', { size: 80, color: C.red });
    return (t) => {
      charsPop(h, t, Wt('bosses') - .2, .045);
      tf(rep, 540, drop(t, Wt('reportedly') - .1, 400, .3), 1, -1);
      ex.forEach((e, k) => tf(e, 270 + k * 270, drop(t, K.c5 + .1 + k * .08, 930), .9));
      tf(table, 540, drop(t, K.c5 + .05, 1010));
      tf(cam, 540, drop(t, Wt('shows') - .1, 900), .45, -3);
      tf(b1, 330, drop(t, Wt('thats') - .15, 560, .3), 1, -3);
      tf(b2, 600, drop(t, Wt('dont') - .25, 700, .3), 1, 2);
      stampAnim(st, t, Wt('anyone') + .1, 540, 1150, -8);
    };
  });
  // ---------- S9  WHY HIDE IT? KODAK MADE ITS MONEY FROM FILM ----------
  scene(K.c6, K.c7, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.yellow, step: 22, angle: 15, f: radial(540, 820, 760, 1.0), maxK: .64 }).setAttribute('class', 'mul');
    const h = head(g, 'WHY HIDE IT?', 300);
    const fr = filmRoll(g);
    const bills = []; const rr = rng(12); for (let k = 0; k < 12; k++) bills.push([bill(g), k % 2 ? 110 + rr() * 150 : 840 + rr() * 150, 520 + rr() * 520, (rr() - .5) * 40, rr() * .4]);
    const ev = el('g', {}, g); el('rect', { x: -400, y: -80, width: 800, height: 160, fill: C.cream, stroke: C.ink, 'stroke-width': 6, transform: 'rotate(-2)' }, ev);
    txt(ev, '1976: KODAK SOLD 90% OF', { x: 0, y: -12, 'font-size': 44, 'font-family': F.slab, fill: C.ink, 'text-anchor': 'middle' });
    txt(ev, 'ALL FILM IN THE US', { x: 0, y: 46, 'font-size': 44, 'font-family': F.slab, fill: C.red, 'text-anchor': 'middle' });
    el('rect', { x: -60, y: -100, width: 120, height: 36, fill: 'rgba(248,190,140,.75)', transform: 'rotate(-4)' }, ev);
    return (t) => {
      charsPop(h, t, K.c6 + .02, .045);
      tf(fr, 470, drop(t, Wt('kodak', 2) - .2, 800), 1, -4);
      bills.forEach(([b, x, y, r, d]) => { const t0 = Wt('money') + d; op(b, t > t0 ? 1 : 0); tf(b, x, lerp(y - 500, y, E.out(seg(t, t0, t0 + .4))), .9, r); });
      tf(ev, 540, drop(t, Wt('film') + .05, 1150, .35));
    };
  });
  // ---------- S10  THE MONEY LOOP: film -> developing -> prints -> $ ; digital breaks it ----------
  scene(K.c7, K.c8, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.orange, step: 22, angle: 15, f: radial(540, 820, 700, 1.0), maxK: .6 }).setAttribute('class', 'mul');
    const h = head(g, 'THE MONEY LOOP', 300);
    const ring = el('circle', { cx: 540, cy: 830, r: 300, fill: 'none', stroke: C.ink, 'stroke-width': 10, 'stroke-dasharray': '34 22' }, g);
    const N = [['FILM', 'film', 1, 540, 530], ['DEVELOPING', 'developing', 0, 880, 830], ['PRINTS', 'prints', 0, 540, 1130], ['$$$', 'prints', 0, 200, 830]].map(([s, w, n, x, y], i) => {
      const c = el('g', {}, g); const card = el('rect', { x: -150, y: -62, width: 300, height: 124, rx: 16, fill: C.cream, stroke: C.ink, 'stroke-width': 7 }, c);
      txt(c, s, { x: 0, y: 16, 'font-size': s.length > 6 ? 38 : 60, 'font-family': F.bagel, fill: C.ink, 'text-anchor': 'middle' }); const xm = xmark(c, 70);
      return { c, card, xm, t0: Wt(w, n) + (i === 3 ? .45 : -.1), x, y }; });
    const dig = tag(g, 'DIGITAL PHOTO', { size: 34, fill: C.orange });
    const kill = [[0, Wt('no') - .05], [1, Wt('no', 1) - .2], [2, Wt('no', 1) - .05], [3, Wt('repeat') - .1]];
    const st = stampEl(g, 'NO REPEAT BUSINESS', { size: 78, color: C.red });
    return (t) => {
      charsPop(h, t, K.c7 + .02, .04);
      tf(ring, 0, 0); ring.setAttribute('stroke-dashoffset', (-t * 120).toFixed(0)); op(ring, t > Wt('film', 1) - .2 ? 1 : 0);
      N.forEach(n => { tf(n.c, n.x, n.y, pop(t, n.t0, .3) || .001); n.card.setAttribute('fill', t > n.t0 && t < Wt('digital', 2) ? C.yellow : C.cream); });
      tf(dig, 540, 830, pop(t, Wt('digital', 2) - .1, .3) || .001);
      kill.forEach(([i, t0]) => N[i].xm.draw(t, t0));
      stampAnim(st, t, Wt('business') + .1, 540, 1260, -6);
    };
  });
  // ---------- S11  KODAK PROTECTED THE PAST, WHILE THE FUTURE QUIETLY LOADED ----------
  scene(K.c8, K.ph, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.teal, step: 22, angle: 15, f: radial(540, 760, 640, 1.0), maxK: .6 }).setAttribute('class', 'mul');
    const h = head(g, 'GUARDING FILM', 300);
    const an = tag(g, 'ANALYSIS', { size: 30, fill: C.ink, col: C.yellow });
    const fo = folder(g, 'FILM BUSINESS');
    const lock = el('g', { filter: 'url(#boil)' }, g); el('path', { d: 'M-60 -30 L-60 -90 C-60 -150 60 -150 60 -90 L60 -30', fill: 'none', stroke: C.ink, 'stroke-width': 22 }, lock);
    el('rect', { x: -95, y: -40, width: 190, height: 150, rx: 18, fill: C.red, stroke: C.ink, 'stroke-width': 8 }, lock); el('circle', { cx: 0, cy: 30, r: 18, fill: C.ink }, lock);
    const fut = txt(g, 'THE FUTURE', { x: 0, y: 0, 'font-size': 52, 'font-family': F.slab, fill: C.ink });
    const barBg = el('rect', { x: 0, y: 0, width: 760, height: 64, rx: 16, fill: C.cream, stroke: C.ink, 'stroke-width': 7 }, g);
    const bar = el('rect', { x: 0, y: 0, width: 0, height: 64, rx: 16, fill: C.orange, stroke: C.ink, 'stroke-width': 7 }, g);
    const pct = txt(g, '0%', { x: 0, y: 0, 'font-size': 52, 'font-family': F.bagel, fill: C.ink, 'text-anchor': 'end' });
    return (t) => {
      charsPop(h, t, Wt('protected') - .15, .04);
      tf(an, 900, drop(t, K.c8 + .1, 400, .3), 1, 3);
      tf(fo.g, 540, drop(t, K.c8 + .05, 760), 1, -2); tf(lock, 540, lerp(-300, 860, E.back(seg(t, Wt('past') - .2, Wt('past') + .15))), .9);
      const show2 = t > Wt('future') - .2; [fut, barBg, bar, pct].forEach(e => op(e, show2 ? 1 : 0));
      tf(fut, 160, 1110); tf(barBg, 160, 1140); tf(bar, 160, 1140); tf(pct, 920, 1110);
      const p = E.io(seg(t, Wt('future'), Wt('loaded') + .3)); bar.setAttribute('width', (760 * p).toFixed(0)); pct.textContent = Math.round(p * 100) + '%';
    };
  });
  // ---------- S12  SMARTPHONES PUT A CAMERA IN EVERYONE'S POCKET ----------
  scene(K.ph, K.c9, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.yellow, step: 22, angle: 15, f: radial(540, 820, 760, .9), maxK: .64 }).setAttribute('class', 'mul');
    halftone(g, { color: C.orange, step: 20, angle: 60, f: edge(1000, 1.4), maxK: .6 }).setAttribute('class', 'mul');
    const h = head(g, 'SMARTPHONES', 300);
    const P = []; for (let k = 0; k < 6; k++) P.push(phone(g, .62));
    const st = stampEl(g, 'A CAMERA IN EVERY POCKET', { size: 62, color: C.red });
    return (t) => {
      charsPop(h, t, Wt('smartphones') - .15, .04);
      P.forEach((p, k) => { const t0 = Wt('smartphones') + k * .1; tf(p, 220 + (k % 3) * 320, (k < 3 ? 640 : 1000) + 2300 * (1 - E.back(seg(t, t0, t0 + .35))), 1, (k % 2 ? 6 : -6)); });
      stampAnim(st, t, Wt('pocket') + .05, 540, 820, -7);
    };
  });
  // ---------- S13  2012: KODAK FILES FOR BANKRUPTCY ----------
  scene(K.c9, K.ir, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.red, step: 22, angle: 15, f: edge(950, 1.1), maxK: .64 }).setAttribute('class', 'mul');
    const h = head(g, 'JANUARY 2012', 300);
    const np = el('g', { filter: 'url(#boil)' }, g); el('rect', { x: -400, y: -360, width: 800, height: 720, rx: 8, fill: '#FBF6EC', stroke: C.ink, 'stroke-width': 8 }, np);
    txt(np, 'BUSINESS NEWS', { x: 0, y: -270, 'font-size': 66, 'font-family': F.slab, fill: C.ink, 'text-anchor': 'middle' });
    el('line', { x1: -360, x2: 360, y1: -240, y2: -240, stroke: C.ink, 'stroke-width': 6 }, np);
    txt(np, 'JANUARY 19, 2012', { x: 0, y: -200, 'font-size': 28, 'font-family': F.mono, 'font-weight': 800, fill: '#9C8676', 'text-anchor': 'middle' });
    txt(np, 'KODAK FILES', { x: 0, y: -80, 'font-size': 92, 'font-family': F.bagel, fill: C.ink, 'text-anchor': 'middle' });
    txt(np, 'FOR BANKRUPTCY', { x: 0, y: 20, 'font-size': 76, 'font-family': F.bagel, fill: C.red, 'text-anchor': 'middle' });
    for (let k = 0; k < 6; k++) el('rect', { x: -360, y: 80 + k * 42, width: k % 3 === 2 ? 460 : 720, height: 18, rx: 6, fill: '#D9C9B8' }, np);
    txt(np, 'ILLUSTRATION', { x: 360, y: 340, 'font-size': 22, 'font-family': F.mono, 'font-weight': 800, fill: '#9C8676', 'text-anchor': 'end' });
    const st = stampEl(g, 'BANKRUPT', { size: 160, color: C.red });
    return (t) => {
      charsPop(h, t, Wt('2012') - .1, .04);
      tf(np, 540, drop(t, Wt('kodak', 4) - .2, 830), 1, lerp(-12, -2, E.out(seg(t, Wt('kodak', 4) - .2, Wt('kodak', 4) + .4))));
      stampAnim(st, t, Wt('bankruptcy') + .1, 600, 1120, -8);
    };
  });
  // ---------- S14  THE IRONY: disrupted by its own invention ----------
  scene(K.ir, K.c10, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.yellow, step: 22, angle: 15, f: radial(540, 820, 700, 1.0), maxK: .6 }).setAttribute('class', 'mul');
    const h = head(g, 'THE IRONY', 300);
    const cam = proto(g); const l1 = tag(g, 'INVENTED BY KODAK', { size: 32, fill: C.orange });
    const bld = el('g', { filter: 'url(#boil)' }, g); el('rect', { x: -170, y: -380, width: 340, height: 600, rx: 10, fill: C.cream, stroke: C.ink, 'stroke-width': 8 }, bld);
    for (let r = 0; r < 7; r++) for (let c = 0; c < 3; c++) el('rect', { x: -125 + c * 90, y: -330 + r * 74, width: 60, height: 46, rx: 6, fill: C.ink }, bld);
    el('rect', { x: -170, y: -440, width: 340, height: 70, rx: 8, fill: C.red, stroke: C.ink, 'stroke-width': 8 }, bld);
    txt(bld, 'KODAK', { x: 0, y: -390, 'font-size': 52, 'font-family': F.slab, fill: C.cream, 'text-anchor': 'middle' });
    const crack = el('path', { d: 'M-20 -380 L30 -260 L-30 -150 L40 -30 L-20 90 L30 220', fill: 'none', stroke: C.red, 'stroke-width': 14, 'stroke-linejoin': 'round', 'stroke-dasharray': 800, 'stroke-dashoffset': 800 }, bld);
    const arr = el('path', { d: 'M340 760 C420 560 620 540 690 620', fill: 'none', stroke: C.red, 'stroke-width': 12, 'stroke-dasharray': 520, 'stroke-dashoffset': 520, 'stroke-linecap': 'round' }, g);
    const head2 = el('path', { d: 'M0 0 L-40 -10 L-14 30 Z', fill: C.red }, g);
    const st = stampEl(g, 'DISRUPTED', { size: 104, color: C.red });
    return (t) => {
      charsPop(h, t, K.ir + .02, .05);
      tf(cam, 300, drop(t, Wt('invented', 1) - .2, 880), .6, -4); tf(l1, 300, drop(t, Wt('invented', 1), 1040, .3));
      const sh = t > Wt('disrupted') ? Math.sin(t * 70) * 10 * Math.exp(-(t - Wt('disrupted')) * 3) : 0;
      tf(bld, 790 + sh, drop(t, K.ir + .1, 1000), .85, t > Wt('disrupted') ? lerp(0, 5, E.out(seg(t, Wt('disrupted'), Wt('disrupted') + .5))) : 0);
      crack.setAttribute('stroke-dashoffset', (800 * (1 - E.out(seg(t, Wt('disrupted'), Wt('disrupted') + .35)))).toFixed(0));
      const a = seg(t, Wt('photography') - .2, Wt('disrupted')); arr.setAttribute('stroke-dashoffset', (520 * (1 - E.out(a))).toFixed(0)); op(head2, a > .95 ? 1 : 0); tf(head2, 690, 620, 1, 40);
      stampAnim(st, t, Wt('disrupted') + .1, 540, 1190, -7);
    };
  });
  // ---------- S15  THE LESSON ----------
  scene(K.c10, K.c11, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.orange, step: 22, angle: 15, f: radial(900, 420, 600, 1.1), maxK: .6 }).setAttribute('class', 'mul');
    const h = head(g, 'THE LESSON', 300);
    const card = (s1, s2, col) => { const c = el('g', { filter: 'url(#boil)' }, g); el('rect', { x: -420, y: -130, width: 840, height: 260, rx: 18, fill: C.cream, stroke: C.ink, 'stroke-width': 8 }, c);
      txt(c, s1, { x: -280, y: -20, 'font-size': 56, 'font-family': F.slab, fill: C.ink }); txt(c, s2, { x: -280, y: 60, 'font-size': 56, 'font-family': F.slab, fill: col });
      const badge = el('g', {}, c); tf(badge, -350, 0); return { c, badge }; };
    const A = card('COULD SEE', 'THE FUTURE', C.green), Bc = card('TOO AFRAID TO', 'LOSE THE PRESENT', C.red);
    el('circle', { r: 46, fill: C.green, stroke: C.ink, 'stroke-width': 6 }, A.badge); txt(A.badge, '✓', { x: 0, y: 20, 'font-size': 60, 'font-family': F.sans, 'font-weight': 900, fill: C.cream, 'text-anchor': 'middle' });
    el('circle', { r: 46, fill: C.red, stroke: C.ink, 'stroke-width': 6 }, Bc.badge); txt(Bc.badge, '!', { x: 0, y: 24, 'font-size': 66, 'font-family': F.bagel, fill: C.cream, 'text-anchor': 'middle' });
    const st = stampEl(g, 'REAL CAUSE', { size: 84, color: C.red });
    return (t) => {
      charsPop(h, t, K.c10 + .02, .045);
      tf(A.c, 540, drop(t, Wt('see') - .2, 620), .95, -2);
      tf(Bc.c, 540, drop(t, Wt('afraid') - .25, 960), .95, 1.5);
      stampAnim(st, t, Wt('present') + .05, 700, 1150, -8);
    };
  });
  // ---------- S16  CASE CLOSED + subscribe ----------
  scene(K.c11, K.end + 1, (g) => {
    bg(g, C.paper);
    halftone(g, { color: C.yellow, step: 22, angle: 15, f: radial(540, 760, 760, .9), maxK: .62 }).setAttribute('class', 'mul');
    const fo = folder(g, 'KODAK 1975-2012'); const cc = stampEl(g, 'CASE CLOSED', { size: 110, color: C.red });
    const brand = chars(g, 'TechDecoded', { x: 540, y: 300, size: 110, family: F.slab, weight: 400, fill: C.ink, anchor: 'middle', shadow: { fill: C.orange, dx: 7, dy: 7 } });
    const wm = chars(g, 'with Max', { x: 540, y: 400, size: 70, family: F.bagel, weight: 400, fill: C.orange, anchor: 'middle' });
    const btn = el('g', {}, g); el('rect', { x: -300, y: -70, width: 600, height: 140, rx: 70, fill: '#A8301A' }, btn); const btR = el('rect', { x: -300, y: -84, width: 600, height: 140, rx: 70, fill: 'url(#hlg)', stroke: C.ink, 'stroke-width': 7 }, btn);
    const btT = txt(btn, 'SUBSCRIBE', { x: 0, y: 8, 'font-size': 70, 'font-family': F.sans, 'font-weight': 900, fill: '#FFFFFF', 'text-anchor': 'middle' });
    const cur = el('path', { d: 'M0 0 L0 90 L24 68 L42 108 L58 100 L40 62 L72 62 Z', fill: C.cream, stroke: C.ink, 'stroke-width': 6, 'stroke-linejoin': 'round' }, g);
    return (t) => {
      tf(fo.g, 540, drop(t, K.c11 + .02, 780), .9, -3); stampAnim(cc, t, K.c11 + .6, 540, 790, -10);
      charsPop(brand, t, Wt('techdecoded') - .1, .04); charsPop(wm, t, Wt('techdecoded') + .3, .04);
      const tc = Wt('more') + .1; tf(btn, 540, lerp(2300, 1150, E.back(seg(t, Wt('subscribe') - .1, Wt('subscribe') + .3))), t > tc && t < tc + .12 ? .94 : 1);
      if (t > tc) { btT.textContent = 'SUBSCRIBED ✓'; btR.setAttribute('fill', C.ink); } else { btT.textContent = 'SUBSCRIBE'; btR.setAttribute('fill', 'url(#hlg)'); }
      op(cur, t > Wt('subscribe') + .3 ? 1 : 0); tf(cur, lerp(980, 640, E.out(seg(t, Wt('subscribe') + .3, tc))), lerp(1500, 1160, E.out(seg(t, Wt('subscribe') + .3, tc))), t > tc && t < tc + .12 ? .85 : 1);
    };
  });
