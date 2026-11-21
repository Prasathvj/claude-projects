import React from 'react';
import {interpolate, Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, F} from './theme';
import {cardStyle, clamp, Sfx, useLayout, useSpring} from './motion';

/* ------------------------------------------------------------------ Counter */
/** Number that ticks from `from` to `to` with motion blur while moving; ticks are audible. */
export const Counter: React.FC<{
  from?: number; to: number; decimals?: number; prefix?: string; suffix?: string; size?: number; color?: string;
  start?: number; frames?: number; ticks?: boolean;
}> = ({from = 0, to, decimals = 0, prefix = '', suffix = '', size = 300, color = C.cyan, start = 3, frames = 26, ticks = true}) => {
  const frame = useCurrentFrame();
  const {u} = useLayout();
  const ease = Easing.out(Easing.cubic);
  const p = interpolate(frame, [start, start + frames], [0, 1], {...clamp, easing: ease});
  const pPrev = interpolate(frame - 1, [start, start + frames], [0, 1], {...clamp, easing: ease});
  const val = from + (to - from) * p;
  const speed = Math.abs(p - pPrev) * 40;
  const shown = val.toFixed(decimals);
  const landed = useSpring(start + frames, {damping: 8, stiffness: 260});
  const scale = frame >= start + frames ? 1 + 0.18 * (1 - landed) : 1;
  const tickCount = Math.min(12, Math.max(4, Math.abs(to - from) * (decimals ? 1 : 1)));
  return (
    <div style={{position: 'relative', fontFamily: F.display, fontWeight: 900, fontSize: size * u, color, lineHeight: 1,
      transform: `scale(${scale})`, fontVariantNumeric: 'tabular-nums', textShadow: `0 0 ${40 * u}px ${color}66`, whiteSpace: 'nowrap'}}>
      <span style={{filter: `blur(${Math.min(8, speed * 2) * u}px)`}}>{prefix}{shown}</span>
      <span style={{fontSize: size * 0.38 * u, color: C.white, marginLeft: 8 * u}}>{suffix}</span>
      {speed > 0.2 && (
        <span style={{position: 'absolute', left: 0, top: -speed * 10 * u, opacity: 0.25, filter: `blur(${6 * u}px)`}}>
          {prefix}{shown}
        </span>
      )}
      {ticks && Array.from({length: tickCount}).map((_, i) => (
        <Sfx key={i} name="tick" at={start + (frames * Math.pow(i / tickCount, 1.6))} volume={0.5} />
      ))}
      {ticks && <Sfx name="impact" at={start + frames} volume={0.55} />}
    </div>
  );
};

/* ------------------------------------------------------------------ Receipt / stack */
/** A receipt that prints line by line, then stamps the total. */
export const Receipt: React.FC<{title: string; items: [string, string][]; total: [string, string]; width?: number}> = ({
  title, items, total, width = 760,
}) => {
  const frame = useCurrentFrame();
  const {u} = useLayout();
  const per = 7;
  const n = items.length;
  const unroll = interpolate(frame, [0, 10 + n * per + 10], [0.12, 1], {...clamp, easing: Easing.out(Easing.quad)});
  const stamp = useSpring(14 + n * per, {damping: 9, stiffness: 220});
  const zig = Array.from({length: 24}).map((_, i) => `${(i / 23) * 100}% ${i % 2 ? 100 : 0}%`).join(',');
  return (
    <div style={{width: width * u, position: 'relative'}}>
      <div style={{background: '#F4F7FF', color: C.navy, borderRadius: `${14 * u}px ${14 * u}px 0 0`, padding: `${36 * u}px ${44 * u}px ${30 * u}px`,
        fontFamily: F.mono, clipPath: `inset(0 0 ${(1 - unroll) * 100}% 0)`, boxShadow: `0 ${30 * u}px ${70 * u}px rgba(0,0,0,0.5)`}}>
        <div style={{fontWeight: 700, fontSize: 34 * u, textAlign: 'center', letterSpacing: 3 * u}}>{title}</div>
        <div style={{borderTop: `${3 * u}px dashed #9aa6c8`, margin: `${20 * u}px 0`}} />
        {items.map(([a, b], i) => {
          const s = interpolate(frame, [8 + i * per, 12 + i * per], [0, 1], clamp);
          return (
            <div key={i} style={{display: 'flex', justifyContent: 'space-between', fontSize: 32 * u, padding: `${8 * u}px 0`, opacity: s,
              transform: `translateX(${(1 - s) * -20 * u}px)`}}>
              <span>{a}</span>
              <span style={{fontWeight: 700}}>{b}</span>
            </div>
          );
        })}
        <div style={{borderTop: `${3 * u}px dashed #9aa6c8`, margin: `${20 * u}px 0`}} />
        <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 40 * u, fontWeight: 700}}>
          <span>{total[0]}</span>
          <span style={{color: C.hot, transform: `scale(${0.4 + 0.6 * stamp}) rotate(${(1 - stamp) * -20}deg)`, display: 'inline-block',
            opacity: stamp > 0.02 ? 1 : 0}}>{total[1]}</span>
        </div>
      </div>
      <div style={{height: 22 * u, background: '#F4F7FF', clipPath: `polygon(${zig})`, opacity: unroll > 0.98 ? 1 : 0}} />
      {items.map((_, i) => <Sfx key={i} name="click" at={8 + i * per} volume={0.4} />)}
      <Sfx name="print" at={2} volume={0.5} />
      <Sfx name="impact" at={14 + n * per} volume={0.6} />
    </div>
  );
};

/** Blocks that drop in and stack, the classic "total stacks" build. */
export const Stack: React.FC<{items: string[]; colors?: string[]; width?: number}> = ({items, colors, width = 700}) => {
  const {u} = useLayout();
  const frame = useCurrentFrame();
  const pal = colors || [C.cyan, '#5AA9FF', '#7C8CFF', '#C17CFF', C.hot, C.gold];
  return (
    <div style={{display: 'flex', flexDirection: 'column-reverse', gap: 14 * u, width: width * u}}>
      {items.map((t, i) => {
        const d = 4 + i * 7;
        const s = useSpring(d, {damping: 10, stiffness: 210});
        return (
          <div key={i} style={{transform: `translateY(${(1 - s) * -600 * u}px) rotate(${(1 - s) * (i % 2 ? 6 : -6)}deg)`, opacity: frame < d ? 0 : 1,
            background: pal[i % pal.length], color: C.navy, borderRadius: 18 * u, padding: `${20 * u}px ${30 * u}px`,
            fontFamily: F.display, fontWeight: 900, fontSize: 46 * u, display: 'flex', alignItems: 'center', gap: 20 * u,
            boxShadow: `0 ${12 * u}px 0 rgba(0,0,0,0.25), 0 ${20 * u}px ${40 * u}px rgba(0,0,0,0.35)`}}>
            <span style={{opacity: 0.55, fontSize: 34 * u}}>{String(i + 1).padStart(2, '0')}</span>
            {t}
          </div>
        );
      })}
    </div>
  );
};

/* ------------------------------------------------------------------ Kinetic captions */
type Word = {w: string; s: number; e: number};
/** 1-3 word caption groups; the spoken word lights up cyan; each new group pops. `t` = seconds into the beat. */
export const Captions: React.FC<{words: Word[]; t: number; big?: boolean; hot?: string[]}> = ({words, t, big = true, hot = []}) => {
  const {u, isV, fps} = useLayout();
  const groups: Word[][] = [];
  let cur: Word[] = [];
  words.forEach((w, i) => {
    cur.push(w);
    const brk = /[,.:;!?]$/.test(w.w) || cur.length >= (big ? 3 : 5) || (cur.join('').length > 22 && big);
    if (brk || i === words.length - 1) {
      groups.push(cur);
      cur = [];
    }
  });
  const gi = groups.findIndex((g) => t < g[g.length - 1].e + 0.05);
  if (gi < 0) return null;
  const g = groups[gi];
  const since = Math.max(0, t - g[0].s) * fps;
  const pop = 1 + 0.25 * Math.exp(-since / 2.5) * Math.cos(since / 1.6);
  const size = big ? 92 : 50;
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: isV ? 1300 * u : undefined, bottom: isV ? undefined : 60 * u,
      display: 'flex', justifyContent: 'center', padding: `0 ${60 * u}px`}}>
      <div style={{transform: `scale(${pop})`, textAlign: 'center', fontFamily: F.display, fontWeight: 900, fontSize: size * u, lineHeight: 1.08,
        textTransform: big ? 'uppercase' : 'none', letterSpacing: big ? -1 * u : 0,
        background: big ? 'transparent' : 'rgba(11,18,38,0.78)', padding: big ? 0 : `${10 * u}px ${22 * u}px`, borderRadius: 14 * u}}>
        {g.map((w, i) => {
          const on = t >= w.s - 0.02;
          const clean = w.w.replace(/[^a-z0-9']/gi, '').toLowerCase();
          const isHot = hot.includes(clean);
          return (
            <span key={i} style={{color: on ? (isHot ? C.hot : C.cyan) : C.white, marginRight: (big ? 22 : 12) * u,
              WebkitTextStroke: big ? `${10 * u}px ${C.navy}` : undefined, paintOrder: 'stroke fill',
              textShadow: big ? `0 ${8 * u}px 0 rgba(0,0,0,0.45)` : undefined}}>
              {w.w}
            </span>
          );
        })}
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------ Code window */
type Line = {t: string; c?: string};
const lineColor = (c?: string) => ({cyan: C.cyan, hot: C.hot, dim: C.dim, text: C.white, gold: C.gold, green: C.green} as any)[c || 'text'] || C.white;
/** Editor window that types its lines; hot lines glow red once typed. */
export const CodeWindow: React.FC<{file: string; lines: Line[]; width?: number; cps?: number}> = ({file, lines, width = 1300, cps = 2.2}) => {
  const frame = useCurrentFrame();
  const {u} = useLayout();
  let budget = Math.max(0, (frame - 6) * cps * 2.2);
  return (
    <div style={{...cardStyle(u), width: width * u, overflow: 'hidden', borderRadius: 22 * u}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 12 * u, padding: `${18 * u}px ${24 * u}px`, background: 'rgba(0,0,0,0.25)',
        borderBottom: `${2 * u}px solid ${C.line}`}}>
        {[C.hot, C.gold, C.green].map((c) => <div key={c} style={{width: 18 * u, height: 18 * u, borderRadius: 99, background: c}} />)}
        <div style={{marginLeft: 16 * u, fontFamily: F.mono, fontSize: 24 * u, color: C.dim}}>{file}</div>
      </div>
      <div style={{padding: `${26 * u}px ${30 * u}px`, fontFamily: F.mono, fontSize: 34 * u, lineHeight: 1.55}}>
        {lines.map((l, i) => {
          const take = Math.min(l.t.length, Math.floor(budget));
          budget -= l.t.length + 6;
          const done = take >= l.t.length;
          const typing = take > 0 && !done;
          const hot = l.c === 'hot';
          return (
            <div key={i} style={{display: 'flex', gap: 22 * u, whiteSpace: 'pre', minHeight: 34 * 1.55 * u,
              background: hot && done ? 'rgba(255,77,109,0.13)' : 'transparent', margin: `0 ${-30 * u}px`, padding: `0 ${30 * u}px`,
              boxShadow: hot && done ? `inset ${6 * u}px 0 0 ${C.hot}` : undefined}}>
              <span style={{color: C.line, width: 40 * u, textAlign: 'right'}}>{i + 1}</span>
              <span style={{color: lineColor(l.c), fontWeight: hot ? 700 : 400}}>
                {l.t.slice(0, take)}
                {(typing || (take === 0 && budget > -l.t.length - 6 && i > 0 && false)) && (
                  <span style={{background: C.cyan, color: C.cyan, opacity: frame % 16 < 8 ? 1 : 0.2}}>▌</span>
                )}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------ UI mockups */
/** Browser window with page text; `reveal` sweeps a select-all highlight that exposes hidden lines. */
export const BrowserCard: React.FC<{url: string; title: string; body: string[]; hidden?: string[]; reveal?: boolean; width?: number}> = ({
  url, title, body, hidden = [], reveal, width = 900,
}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const {u} = useLayout();
  const at = Math.round(durationInFrames * 0.3);
  const sel = reveal ? interpolate(frame, [at, at + 8], [0, 1], clamp) : 0;
  const shake = reveal && frame > at + 6 && frame < at + 16 ? Math.sin(frame * 3) * 6 * u : 0;
  const lineStyle = (i: number): React.CSSProperties => ({
    fontFamily: F.ui, fontWeight: 500, fontSize: 36 * u, color: '#2b3557', padding: `${6 * u}px ${8 * u}px`,
    background: sel > i * 0.15 ? 'rgba(46,140,255,0.35)' : 'transparent', borderRadius: 4 * u,
  });
  return (
    <div style={{width: width * u, borderRadius: 26 * u, overflow: 'hidden', background: '#FFFFFF', transform: `translateX(${shake}px)`,
      boxShadow: `0 ${40 * u}px ${100 * u}px rgba(0,0,0,0.6), 0 0 0 ${2 * u}px rgba(255,255,255,0.4)`}}>
      <div style={{background: '#E7ECF7', padding: `${18 * u}px ${22 * u}px`, display: 'flex', alignItems: 'center', gap: 12 * u}}>
        {[C.hot, C.gold, C.green].map((c) => <div key={c} style={{width: 18 * u, height: 18 * u, borderRadius: 99, background: c}} />)}
        <div style={{flex: 1, marginLeft: 14 * u, background: '#FFFFFF', borderRadius: 99, padding: `${8 * u}px ${22 * u}px`, fontFamily: F.ui,
          fontWeight: 500, fontSize: 24 * u, color: '#56607f'}}>🔒 {url}</div>
      </div>
      <div style={{padding: `${34 * u}px ${44 * u}px ${44 * u}px`}}>
        <div style={{height: 180 * u, borderRadius: 18 * u, background: 'linear-gradient(135deg,#FFD9A8,#FFB37A)', marginBottom: 26 * u,
          display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 110 * u}}>🥞</div>
        <div style={{fontFamily: F.display, fontWeight: 900, fontSize: 52 * u, color: '#111a33', marginBottom: 14 * u, lineHeight: 1.1}}>{title}</div>
        {body.map((b, i) => <div key={i} style={lineStyle(i)}>{b}</div>)}
        {hidden.map((h, i) => {
          const on = sel > 0.55 + i * 0.15;
          return (
            <div key={'h' + i} style={{...lineStyle(body.length + i), color: on ? C.hot : '#FFFFFF', fontWeight: 600, fontFamily: F.mono,
              fontSize: 32 * u, background: on ? 'rgba(46,140,255,0.35)' : 'transparent', textShadow: on ? `0 0 ${18 * u}px rgba(255,77,109,0.5)` : undefined}}>
              {h}
            </div>
          );
        })}
      </div>
    </div>
  );
};

/** Chat thread: bubbles pop in one by one. */
export const ChatCard: React.FC<{msgs: {from: string; text: string}[]; width?: number}> = ({msgs, width = 860}) => {
  const {u} = useLayout();
  const frame = useCurrentFrame();
  return (
    <div style={{...cardStyle(u), width: width * u, padding: 34 * u, display: 'flex', flexDirection: 'column', gap: 22 * u}}>
      <div style={{fontFamily: F.ui, fontWeight: 600, fontSize: 26 * u, color: C.dim, letterSpacing: 2 * u}}>AI AGENT · CHAT</div>
      {msgs.map((m, i) => {
        const d = 4 + i * 14;
        const s = useSpring(d, {damping: 12, stiffness: 200});
        const you = m.from === 'you';
        return (
          <div key={i} style={{alignSelf: you ? 'flex-end' : 'flex-start', maxWidth: '82%', opacity: frame < d ? 0 : 1,
            transform: `scale(${0.6 + 0.4 * s}) translateY(${(1 - s) * 30 * u}px)`, transformOrigin: you ? 'right bottom' : 'left bottom',
            background: you ? C.cyan : C.navy, color: you ? C.navy : C.white, border: you ? 'none' : `${2 * u}px solid ${C.line}`,
            borderRadius: 30 * u, padding: `${22 * u}px ${30 * u}px`, fontFamily: F.ui, fontWeight: 600, fontSize: 40 * u}}>
            {m.text}
          </div>
        );
      })}
      {msgs[msgs.length - 1]?.from === 'you' && frame > 4 + msgs.length * 14 && (
        <div style={{alignSelf: 'flex-start', background: C.navy, border: `${2 * u}px solid ${C.line}`, borderRadius: 30 * u,
          padding: `${22 * u}px ${30 * u}px`, display: 'flex', gap: 12 * u}}>
          {[0, 1, 2].map((i) => (
            <div key={i} style={{width: 18 * u, height: 18 * u, borderRadius: 99, background: C.cyan,
              opacity: 0.3 + 0.7 * Math.max(0, Math.sin((frame - i * 4) / 4))}} />
          ))}
          <span style={{fontFamily: F.ui, fontWeight: 600, fontSize: 30 * u, color: C.dim, marginLeft: 8 * u}}>reading page…</span>
        </div>
      )}
    </div>
  );
};

/** Email preview with an optional hidden line that is revealed as a red overlay. */
export const EmailCard: React.FC<{from: string; subject: string; body: string[]; hidden?: string[]; width?: number}> = ({
  from, subject, body, hidden = [], width = 900,
}) => {
  const {u} = useLayout();
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const at = Math.round(durationInFrames * 0.45);
  const on = interpolate(frame, [at, at + 6], [0, 1], clamp);
  return (
    <div style={{width: width * u, borderRadius: 26 * u, background: '#FFFFFF', overflow: 'hidden',
      boxShadow: `0 ${40 * u}px ${100 * u}px rgba(0,0,0,0.6)`}}>
      <div style={{background: '#E7ECF7', padding: `${22 * u}px ${30 * u}px`, fontFamily: F.ui, fontWeight: 600, fontSize: 26 * u, color: '#56607f',
        display: 'flex', justifyContent: 'space-between'}}>
        <span>✉ Inbox</span><span>1 new</span>
      </div>
      <div style={{padding: `${30 * u}px ${40 * u}px ${40 * u}px`, fontFamily: F.ui}}>
        <div style={{fontSize: 28 * u, color: '#56607f', fontWeight: 500}}>From: {from}</div>
        <div style={{fontSize: 44 * u, color: '#111a33', fontWeight: 600, margin: `${10 * u}px 0 ${20 * u}px`}}>{subject}</div>
        {body.map((b, i) => <div key={i} style={{fontSize: 34 * u, color: '#2b3557', fontWeight: 500, marginBottom: 10 * u}}>{b}</div>)}
        {[0, 1].map((i) => <div key={'l' + i} style={{height: 22 * u, width: `${88 - i * 20}%`, background: '#E7ECF7', borderRadius: 8 * u, margin: `${14 * u}px 0`}} />)}
        {hidden.map((h, i) => (
          <div key={'h' + i} style={{marginTop: 14 * u, fontFamily: F.mono, fontSize: 30 * u, fontWeight: 700, color: on > 0.5 ? C.hot : '#FFFFFF',
            background: `rgba(255,77,109,${0.12 * on})`, border: `${3 * u}px dashed rgba(255,77,109,${on})`, borderRadius: 10 * u,
            padding: `${10 * u}px ${16 * u}px`}}>{h}</div>
        ))}
      </div>
    </div>
  );
};
