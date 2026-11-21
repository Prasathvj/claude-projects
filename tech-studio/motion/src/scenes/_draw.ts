// Stick Dude drawing kit on top of the pdoom toolkit: hairline primitives in world px (y down),
// traced outlines (a polyline revealed by a pen), line-art icons and the agent character.
// Everything is a pure function of t.
import { rgba } from '../engine/palette';
import { F, font, measure } from '../engine/type';
import { clamp, ease, lerp, noise1, prog, TAU } from '../engine/util';
import { type Cam, type P, pt, lengths, at, rectPts, arc } from './_vo';

export const ARCH = (wd: number, wt: number) => F.archivo(wd, wt);
export type Ctx = CanvasRenderingContext2D;

/** Hairline width in world units for a camera (1 screen px * k). */
export const hair = (c: Cam, k = 1) => (1.2 * k) / c.z;

export function rrPts(x: number, y: number, w: number, h: number, r: number, n = 6): P[] {
  r = Math.min(r, w / 2, h / 2);
  const out: P[] = [];
  const corner = (cx: number, cy: number, a0: number) => { for (let i = 0; i <= n; i++) { const a = a0 + (i / n) * (Math.PI / 2); out.push(pt(cx + r * Math.cos(a), cy + r * Math.sin(a))); } };
  corner(x + w - r, y + r, -Math.PI / 2);
  corner(x + w - r, y + h - r, 0);
  corner(x + r, y + h - r, Math.PI / 2);
  corner(x + r, y + r, Math.PI);
  out.push(out[0]!);
  return out;
}

/** Draw the first `k` (0..1) of a polyline; returns the head point (for the pen). */
export function trace(ctx: Ctx, ps: P[], k: number, stroke: string, width: number): P | null {
  if (k <= 0) return null;
  const L = lengths(ps), tot = L[L.length - 1]!;
  const s = tot * clamp(k);
  ctx.beginPath();
  ctx.moveTo(ps[0]!.x, ps[0]!.y);
  let head: P = ps[0]!;
  for (let i = 1; i < ps.length; i++) {
    if (L[i]! <= s) { ctx.lineTo(ps[i]!.x, ps[i]!.y); head = ps[i]!; continue; }
    const h = at(ps, L, s); ctx.lineTo(h.x, h.y); head = pt(h.x, h.y); break;
  }
  ctx.strokeStyle = stroke; ctx.lineWidth = width; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  ctx.stroke();
  return k < 1 ? head : null;
}
export const headOf = (ps: P[], k: number): P | null => {
  if (k <= 0 || k >= 1) return null;
  const L = lengths(ps); const h = at(ps, L, L[L.length - 1]! * k); return pt(h.x, h.y);
};

export function fillRR(ctx: Ctx, x: number, y: number, w: number, h: number, r: number, fill: string) {
  ctx.beginPath(); ctx.roundRect(x, y, w, h, r); ctx.fillStyle = fill; ctx.fill();
}
export function strokeRR(ctx: Ctx, x: number, y: number, w: number, h: number, r: number, stroke: string, width: number, dash: number[] = []) {
  ctx.beginPath(); ctx.roundRect(x, y, w, h, r); ctx.setLineDash(dash); ctx.strokeStyle = stroke; ctx.lineWidth = width; ctx.stroke(); ctx.setLineDash([]);
}

/** Text helper: family, size, colour, alignment, letter spacing; returns width. */
export function text(ctx: Ctx, s: string, x: number, y: number, fam: string, size: number, col: string, o: { align?: CanvasTextAlign; sp?: number; base?: CanvasTextBaseline; stroke?: number } = {}) {
  ctx.font = font(fam, size);
  ctx.letterSpacing = `${o.sp ?? 0}px`;
  ctx.textAlign = o.align ?? 'left';
  ctx.textBaseline = o.base ?? 'alphabetic';
  if (o.stroke) { ctx.lineWidth = o.stroke; ctx.strokeStyle = col; ctx.strokeText(s, x, y); }
  else { ctx.fillStyle = col; ctx.fillText(s, x, y); }
  const w = measure(s, fam, size, o.sp ?? 0);
  ctx.letterSpacing = '0px'; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  return w;
}
/** Spaced mono caps label. */
export const mono = (ctx: Ctx, s: string, x: number, y: number, size: number, col: string, align: CanvasTextAlign = 'left', weight = 500) =>
  text(ctx, s, x, y, F.mono(weight), size, col, { align, sp: size * 0.22 });

/** Typewriter: the first n characters of s (n may be fractional; a caret follows). */
export function typed(s: string, n: number) { return s.slice(0, Math.max(0, Math.floor(n))); }

/** Fit a font size so text spans at most maxW. */
export function fit(s: string, fam: string, maxW: number, max: number, sp = 0) {
  const w = measure(s, fam, 100, sp);
  return Math.min(max, (maxW / Math.max(1, w)) * 100);
}

/** Overshoot pop 0..1 (spring-ish) used for snaps. */
export const pop = (t: number, t0: number, dur = 0.35) => {
  const u = clamp((t - t0) / dur);
  if (u <= 0) return 0;
  return 1 + Math.sin(u * Math.PI * 1.5) * Math.exp(-u * 5) * 0.35 - (1 - ease.outExpo(u)) * 1;
};

// ------------------------------------------------------------------ line-art icons (100x100 box, centred)
export function icon(ctx: Ctx, name: string, cx: number, cy: number, s: number, col: string, w: number) {
  ctx.save();
  ctx.translate(cx, cy); ctx.scale(s / 100, s / 100); ctx.translate(-50, -50);
  ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = (w * 100) / s; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  const P = (d: string) => ctx.stroke(new Path2D(d));
  switch (name) {
    case 'globe': ctx.beginPath(); ctx.arc(50, 50, 34, 0, TAU); ctx.stroke(); ctx.beginPath(); ctx.ellipse(50, 50, 15, 34, 0, 0, TAU); ctx.stroke(); P('M17 39h66M17 61h66'); break;
    case 'mail': ctx.strokeRect(16, 26, 68, 48); P('M18 29l32 25 32-25'); break;
    case 'doc': P('M28 14h30l16 16v56H28z'); P('M58 14v16h16M38 50h26M38 62h26M38 74h18'); break;
    case 'code': P('M36 30L16 50l20 20M64 30l20 20-20 20M56 22L44 78'); break;
    case 'send': P('M14 48l72-30-26 66-12-26z'); P('M48 58l38-40'); break;
    case 'cart': P('M12 22h12l10 40h42l8-28H30'); ctx.beginPath(); ctx.arc(40, 74, 5, 0, TAU); ctx.stroke(); ctx.beginPath(); ctx.arc(70, 74, 5, 0, TAU); ctx.stroke(); break;
    case 'gear': for (let i = 0; i < 8; i++) { const a = (i / 8) * TAU; P(`M${50 + Math.cos(a) * 26} ${50 + Math.sin(a) * 26}L${50 + Math.cos(a) * 36} ${50 + Math.sin(a) * 36}`); } ctx.beginPath(); ctx.arc(50, 50, 24, 0, TAU); ctx.stroke(); ctx.beginPath(); ctx.arc(50, 50, 9, 0, TAU); ctx.stroke(); break;
    case 'shield': P('M50 12l32 12v22c0 22-15 36-32 42-17-6-32-20-32-42V24z'); P('M36 50l10 10 20-22'); break;
    case 'skull': P('M50 14c-22 0-36 15-36 34 0 12 6 20 13 25v13h46V73c7-5 13-13 13-25 0-19-14-34-36-34z'); ctx.beginPath(); ctx.arc(37, 50, 8, 0, TAU); ctx.fill(); ctx.beginPath(); ctx.arc(63, 50, 8, 0, TAU); ctx.fill(); P('M50 60l-5 9h10zM40 86v-8M50 86v-8M60 86v-8'); break;
    case 'server': for (const y of [16, 40, 64]) { ctx.strokeRect(18, y, 64, 20); ctx.beginPath(); ctx.arc(30, y + 10, 3, 0, TAU); ctx.fill(); } break;
    case 'brain': P('M48 18c-8-6-22-3-24 7-10 3-12 15-6 21-5 8 0 20 11 20 3 9 15 12 19 4V18z'); P('M52 18c8-6 22-3 24 7 10 3 12 15 6 21 5 8 0 20-11 20-3 9-15 12-19 4V18z'); break;
    case 'chat': P('M16 22h68v44H46L30 80V66H16z'); for (const x of [36, 50, 64]) { ctx.beginPath(); ctx.arc(x, 44, 3.5, 0, TAU); ctx.fill(); } break;
    case 'warn': P('M50 14l38 68H12z'); P('M50 40v20'); ctx.beginPath(); ctx.arc(50, 70, 3, 0, TAU); ctx.fill(); break;
    case 'user': ctx.beginPath(); ctx.arc(50, 34, 16, 0, TAU); ctx.stroke(); P('M18 86c3-20 16-30 32-30s29 10 32 30'); break;
    case 'lock': ctx.strokeRect(24, 44, 52, 40); P('M34 44V32a16 16 0 0 1 32 0v12'); ctx.beginPath(); ctx.arc(50, 62, 5, 0, TAU); ctx.fill(); break;
    case 'agent': agentGlyph(ctx); break;
    default: ctx.beginPath(); ctx.arc(50, 50, 30, 0, TAU); ctx.stroke();
  }
  ctx.restore();
}
function agentGlyph(ctx: Ctx) {
  ctx.beginPath(); ctx.roundRect(16, 24, 68, 60, 18); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(50, 24); ctx.lineTo(50, 12); ctx.stroke();
  ctx.beginPath(); ctx.arc(50, 10, 4, 0, TAU); ctx.fill();
  ctx.beginPath(); ctx.arc(37, 52, 6, 0, TAU); ctx.fill(); ctx.beginPath(); ctx.arc(63, 52, 6, 0, TAU); ctx.fill();
}

// ------------------------------------------------------------------ the agent character (hairline robot)
/**
 * The channel's agent: a plotter-drawn robot head, centre (cx, cy), height s. `k` traces the outline (0..1),
 * mood calm | scan | evil; `look` -1..1 moves the eyes. Eyes glow (HDR via bloom on bright fills).
 */
export function agent(ctx: Ctx, c: Cam, t: number, cx: number, cy: number, s: number, o: { k?: number; mood?: 'calm' | 'scan' | 'evil'; look?: number } = {}) {
  const k = o.k ?? 1, mood = o.mood ?? 'calm';
  const u = s / 200;
  const w = 156 * u, h = 140 * u, x = cx - w / 2, y = cy - h / 2 + 10 * u;
  const lw = hair(c, 1.6);
  const outline = rrPts(x, y, w, h, 44 * u, 8);
  const evil = mood === 'evil';
  const line = rgba('bone', 0.9);
  trace(ctx, outline, k, line, lw);
  // antenna
  trace(ctx, [pt(cx, y), pt(cx, y - 26 * u)], prog(k, 0.6, 0.8), line, lw);
  if (k > 0.8) {
    ctx.beginPath(); ctx.arc(cx, y - 32 * u, 7 * u, 0, TAU);
    ctx.fillStyle = evil ? rgba('signal', 1) : rgba('bone', 0.6 + 0.4 * Math.abs(Math.sin(t * 3))); ctx.fill();
  }
  // visor
  const vk = prog(k, 0.5, 1);
  if (vk > 0) {
    ctx.globalAlpha = vk;
    ctx.beginPath(); ctx.roundRect(x + 20 * u, y + 30 * u, w - 40 * u, 66 * u, 24 * u);
    ctx.fillStyle = rgba('ink2', 1); ctx.fill(); ctx.strokeStyle = rgba('bone', 0.35); ctx.lineWidth = lw; ctx.stroke();
    const lx = (o.look ?? 0) * 12 * u + (evil ? noise1(t * 30, 3) * 3 * u : 0);
    const blink = !evil && (t * 0.9) % 3.1 > 3.0 ? 0.15 : 1;
    const ey = y + 63 * u;
    for (const dx of [-24, 24]) {
      const ex = cx + dx * u + lx;
      if (evil) {
        ctx.beginPath(); const sgn = Math.sign(dx);
        ctx.moveTo(ex - sgn * 14 * u, ey - 9 * u); ctx.lineTo(ex + sgn * 12 * u, ey); ctx.lineTo(ex - sgn * 14 * u, ey + 7 * u); ctx.closePath();
        ctx.fillStyle = rgba('ember', 1); ctx.fill();
      } else {
        ctx.beginPath(); ctx.ellipse(ex, ey, 9 * u, 13 * u * blink, 0, 0, TAU);
        ctx.fillStyle = mood === 'scan' ? rgba('ember', 1) : rgba('bone', 1); ctx.fill();
      }
    }
    // mouth
    ctx.beginPath();
    if (evil) { ctx.moveTo(cx - 20 * u, y + h - 18 * u); ctx.quadraticCurveTo(cx, y + h - 28 * u, cx + 20 * u, y + h - 18 * u); }
    else { ctx.moveTo(cx - 18 * u, y + h - 24 * u); ctx.quadraticCurveTo(cx, y + h - 13 * u, cx + 18 * u, y + h - 24 * u); }
    ctx.strokeStyle = evil ? rgba('signal', 1) : rgba('bone', 0.7); ctx.lineWidth = lw * 1.4; ctx.stroke();
    // ears
    for (const sx of [-1, 1]) { ctx.beginPath(); ctx.moveTo(cx + sx * (w / 2), cy - 4 * u); ctx.lineTo(cx + sx * (w / 2 + 12 * u), cy - 4 * u); ctx.lineTo(cx + sx * (w / 2 + 12 * u), cy + 22 * u); ctx.lineTo(cx + sx * (w / 2), cy + 22 * u); ctx.strokeStyle = line; ctx.lineWidth = lw; ctx.stroke(); }
    ctx.globalAlpha = 1;
  }
  return headOf(outline, k);
}

/** Torn-edge polygon across a sheet (for the rip transition), seeded. */
export function tornEdge(x0: number, x1: number, y: number, amp: number, n = 28, seed = 1): P[] {
  const out: P[] = [];
  for (let i = 0; i <= n; i++) out.push(pt(lerp(x0, x1, i / n), y + noise1(i * 0.7, seed) * amp + ((i * 7919) % 5 - 2) * amp * 0.25));
  return out;
}

export { rectPts, arc, pt };
