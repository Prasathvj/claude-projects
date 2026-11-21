import React from 'react';
import {AbsoluteFill, Audio, Easing, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, F} from './theme';

/** Layout unit: 1 = 1px on a 1080-wide vertical or 1080-tall horizontal frame. */
export const useLayout = () => {
  const {width, height, fps} = useVideoConfig();
  const u = Math.min(width, height) / 1080;
  return {u, w: width, h: height, isV: height > width, fps};
};

/** Spring with overshoot, starting at `delay` frames. */
export const useSpring = (delay = 0, config: {damping?: number; stiffness?: number; mass?: number} = {}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - delay, fps, config: {damping: 11, stiffness: 170, mass: 0.8, ...config}});
};

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** Character / icon pop-in: scale from 0 with spring overshoot plus a small rotation settle. */
export const PopIn: React.FC<{delay?: number; children: React.ReactNode; style?: React.CSSProperties; from?: number}> = ({
  delay = 0,
  children,
  style,
  from = 0,
}) => {
  const s = useSpring(delay, {damping: 9, stiffness: 190});
  const frame = useCurrentFrame();
  const rot = interpolate(s, [0, 1], [-14, 0]);
  return (
    <div style={{transform: `scale(${from + (1 - from) * s}) rotate(${rot}deg)`, opacity: frame < delay ? 0 : 1, ...style}}>
      {children}
    </div>
  );
};

/** Slide + fade up. */
export const Rise: React.FC<{delay?: number; children: React.ReactNode; dist?: number; style?: React.CSSProperties}> = ({
  delay = 0,
  children,
  dist = 60,
  style,
}) => {
  const s = useSpring(delay, {damping: 14});
  const {u} = useLayout();
  return (
    <div style={{transform: `translateY(${(1 - s) * dist * u}px)`, opacity: Math.min(1, s * 1.6), ...style}}>{children}</div>
  );
};

/** Punch zoom: a fast scale kick on entry, then a slow push-in for the rest of the shot. */
export const PunchZoom: React.FC<{children: React.ReactNode; kick?: number; push?: number}> = ({children, kick = 0.22, push = 0.05}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const s = useSpring(0, {damping: 13, stiffness: 260});
  const slow = interpolate(frame, [0, durationInFrames], [0, push], clamp);
  return <AbsoluteFill style={{transform: `scale(${1 + kick * (1 - s) + slow})`}}>{children}</AbsoluteFill>;
};

/** Gentle drift so nothing is ever static. */
export const Float: React.FC<{children: React.ReactNode; amp?: number; speed?: number; phase?: number; style?: React.CSSProperties}> = ({
  children,
  amp = 8,
  speed = 0.05,
  phase = 0,
  style,
}) => {
  const frame = useCurrentFrame();
  const {u} = useLayout();
  return <div style={{transform: `translateY(${Math.sin(frame * speed + phase) * amp * u}px)`, ...style}}>{children}</div>;
};

/** Whip pan entry: the new shot slams in sideways with motion blur. */
export const Whip: React.FC<{children: React.ReactNode; dir?: 1 | -1}> = ({children, dir = 1}) => {
  const frame = useCurrentFrame();
  const {w} = useLayout();
  const p = interpolate(frame, [0, 7], [1, 0], {...clamp, easing: Easing.out(Easing.cubic)});
  const blur = interpolate(frame, [0, 3, 8], [40, 28, 0], clamp);
  return (
    <AbsoluteFill style={{transform: `translateX(${dir * p * w * 0.6}px) skewX(${-dir * p * 12}deg)`, filter: `blur(${blur}px)`}}>
      {children}
    </AbsoluteFill>
  );
};

/** Rip transition: a torn sheet covers the cut and tears away, revealing the new shot. */
export const Rip: React.FC<{color?: string}> = ({color = C.white}) => {
  const frame = useCurrentFrame();
  const {w, h} = useLayout();
  const p = interpolate(frame, [0, 11], [0, 1], {...clamp, easing: Easing.in(Easing.cubic)});
  if (frame > 12) return null;
  const teeth = 26;
  const pts: string[] = [];
  for (let i = 0; i <= teeth; i++) {
    const y = (i / teeth) * h;
    const x = w * 0.5 + ((i * 7919) % 13 - 6) * 9 + (i % 2 ? 22 : -22);
    pts.push(`${x},${y}`);
  }
  const left = `0,0 ${pts.join(' ')} 0,${h}`;
  const right = `${w},0 ${pts.join(' ')} ${w},${h}`;
  const off = p * w * 0.75;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg width={w} height={h} style={{position: 'absolute'}}>
        <defs>
          <filter id="ripShadow">
            <feDropShadow dx="0" dy="0" stdDeviation="14" floodColor="#000" floodOpacity="0.55" />
          </filter>
        </defs>
        <g filter="url(#ripShadow)">
          <polygon points={left} fill={color} transform={`translate(${-off} ${p * 40}) rotate(${-p * 6} ${w / 2} ${h / 2})`} />
          <polygon points={right} fill={color} transform={`translate(${off} ${-p * 40}) rotate(${p * 6} ${w / 2} ${h / 2})`} />
        </g>
      </svg>
    </AbsoluteFill>
  );
};

/** One sound effect at a frame offset inside the current sequence. */
export const Sfx: React.FC<{name: string; at?: number; volume?: number}> = ({name, at = 0, volume = 0.8}) => (
  <Sequence from={Math.max(0, Math.round(at))} layout="none">
    <Audio src={staticFile(`sfx/${name}.wav`)} volume={volume} />
  </Sequence>
);

/** Small corner chip used to label illustrations, recreations and simplified diagrams. */
export const LabelChip: React.FC<{text: string}> = ({text}) => {
  const {u, isV} = useLayout();
  return (
    <div
      style={{
        position: 'absolute',
        top: (isV ? 150 : 36) * u,
        left: 36 * u,
        padding: `${8 * u}px ${16 * u}px`,
        borderRadius: 10 * u,
        background: 'rgba(255,77,109,0.14)',
        border: `${2 * u}px solid ${C.hot}`,
        color: C.hot,
        fontFamily: F.ui,
        fontWeight: 600,
        fontSize: 24 * u,
        letterSpacing: 2 * u,
      }}
    >
      {text}
    </div>
  );
};

/** Navy stage: drifting grid, two soft glows and a vignette. */
export const Bg: React.FC<{tint?: string}> = ({tint = C.cyan}) => {
  const frame = useCurrentFrame();
  const {u, w, h} = useLayout();
  const g = 90 * u;
  const off = (frame * 0.6 * u) % g;
  return (
    <AbsoluteFill style={{background: C.navy, overflow: 'hidden'}}>
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${C.line}55 ${1.5 * u}px, transparent ${1.5 * u}px), linear-gradient(90deg, ${C.line}55 ${1.5 * u}px, transparent ${1.5 * u}px)`,
          backgroundSize: `${g}px ${g}px`,
          backgroundPosition: `${off}px ${off}px`,
          opacity: 0.6,
        }}
      />
      <div
        style={{
          position: 'absolute',
          width: w * 0.9,
          height: w * 0.9,
          left: w * 0.05 + Math.sin(frame / 70) * 120 * u - w * 0.3,
          top: h * 0.1 + Math.cos(frame / 90) * 80 * u - w * 0.2,
          background: `radial-gradient(circle, ${tint}2a 0%, transparent 62%)`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          width: w * 0.8,
          height: w * 0.8,
          right: -w * 0.25 + Math.cos(frame / 80) * 100 * u,
          bottom: -w * 0.25 + Math.sin(frame / 60) * 90 * u,
          background: `radial-gradient(circle, ${C.hot}1c 0%, transparent 60%)`,
        }}
      />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.55) 100%)'}} />
    </AbsoluteFill>
  );
};

/** Shared card look: navy panel with a cyan rim light and a deep shadow for depth. */
export const cardStyle = (u: number, extra: React.CSSProperties = {}): React.CSSProperties => ({
  background: `linear-gradient(160deg, ${C.navy3} 0%, ${C.navy2} 100%)`,
  border: `${2 * u}px solid ${C.line}`,
  borderRadius: 28 * u,
  boxShadow: `0 ${40 * u}px ${90 * u}px rgba(0,0,0,0.55), 0 0 0 ${1 * u}px rgba(46,230,255,0.08), inset 0 ${2 * u}px 0 rgba(255,255,255,0.06)`,
  ...extra,
});

/** 3D tilt for UI mockups: settles from a steep angle and keeps a slow sway. */
export const Tilt: React.FC<{children: React.ReactNode; rx?: number; ry?: number}> = ({children, rx = 8, ry = -10}) => {
  const frame = useCurrentFrame();
  const s = useSpring(0, {damping: 15, stiffness: 120});
  const ax = rx * (0.4 + 0.6 * (1 - s)) + Math.sin(frame / 40) * 2;
  const ay = ry * (0.4 + 0.6 * (1 - s)) + Math.cos(frame / 50) * 3;
  return (
    <div style={{perspective: 1800, transformStyle: 'preserve-3d'}}>
      <div style={{transform: `rotateX(${ax}deg) rotateY(${ay}deg) scale(${0.85 + 0.15 * s})`, transformStyle: 'preserve-3d'}}>{children}</div>
    </div>
  );
};
