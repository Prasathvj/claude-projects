import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from './theme';

/** Clay-style icon tiles (original artwork, drawn in code). 200x200 viewBox. */
const TILE: Record<string, string> = {
  globe: C.cyan, mail: C.cyan, doc: '#7C8CFF', code: '#7C8CFF', send: C.cyan, cart: C.gold, gear: '#7C8CFF',
  shield: C.green, skull: C.hot, server: '#7C8CFF', brain: '#C17CFF', chat: C.cyan, warn: C.gold, user: '#5AA9FF', agent: C.cyan,
};

const W = '#FFFFFF';
const glyph = (name: string): React.ReactNode => {
  const s = {fill: 'none', stroke: W, strokeWidth: 11, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};
  switch (name) {
    case 'globe':
      return (
        <g {...s}>
          <circle cx={100} cy={100} r={50} />
          <ellipse cx={100} cy={100} rx={22} ry={50} />
          <path d="M52 84h96M52 116h96" />
        </g>
      );
    case 'mail':
      return (
        <g {...s}>
          <rect x={46} y={62} width={108} height={78} rx={10} />
          <path d="M50 70l50 38 50-38" />
        </g>
      );
    case 'doc':
      return (
        <g {...s}>
          <path d="M62 44h50l28 28v84H62z" />
          <path d="M112 44v28h28M78 100h46M78 124h46" />
        </g>
      );
    case 'code':
      return (
        <g {...s}>
          <path d="M78 66l-32 34 32 34M122 66l32 34-32 34M110 56l-20 88" />
        </g>
      );
    case 'send':
      return (
        <g {...s}>
          <path d="M46 98l108-48-40 108-20-44z" />
          <path d="M94 114l60-64" />
        </g>
      );
    case 'cart':
      return (
        <g {...s}>
          <path d="M42 56h20l16 66h64l12-46H70" />
          <circle cx={86} cy={146} r={9} fill={W} />
          <circle cx={134} cy={146} r={9} fill={W} />
        </g>
      );
    case 'gear':
      return (
        <g>
          {Array.from({length: 8}).map((_, i) => (
            <rect key={i} x={90} y={42} width={20} height={30} rx={5} fill={W} transform={`rotate(${i * 45} 100 100)`} />
          ))}
          <circle cx={100} cy={100} r={42} fill={W} />
          <circle cx={100} cy={100} r={17} fill="rgba(0,0,0,0.25)" />
        </g>
      );
    case 'shield':
      return (
        <g {...s}>
          <path d="M100 44l48 18v34c0 32-22 52-48 62-26-10-48-30-48-62V62z" />
          <path d="M78 100l16 16 30-32" />
        </g>
      );
    case 'skull':
      return (
        <g>
          <path d="M100 46c-34 0-56 24-56 54 0 18 8 30 20 38v18h72v-18c12-8 20-20 20-38 0-30-22-54-56-54z" fill={W} />
          <circle cx={78} cy={104} r={14} fill="#3a0d18" />
          <circle cx={122} cy={104} r={14} fill="#3a0d18" />
          <path d="M100 118l-8 14h16z" fill="#3a0d18" />
          <path d="M84 148v8M100 148v8M116 148v8" stroke="#3a0d18" strokeWidth={5} />
        </g>
      );
    case 'server':
      return (
        <g {...s}>
          <rect x={52} y={46} width={96} height={30} rx={8} />
          <rect x={52} y={86} width={96} height={30} rx={8} />
          <rect x={52} y={126} width={96} height={30} rx={8} />
          <path d="M70 61h1M70 101h1M70 141h1" strokeWidth={14} />
        </g>
      );
    case 'brain':
      return (
        <g {...s}>
          <path d="M98 52c-12-10-34-6-38 10-14 4-18 22-8 32-8 12 0 30 16 30 4 14 24 18 30 6V52z" />
          <path d="M102 52c12-10 34-6 38 10 14 4 18 22 8 32 8 12 0 30-16 30-4 14-24 18-30 6V52z" />
        </g>
      );
    case 'chat':
      return (
        <g>
          <path d="M50 60h100a10 10 0 0 1 10 10v54a10 10 0 0 1-10 10H96l-26 22v-22H50a10 10 0 0 1-10-10V70a10 10 0 0 1 10-10z" fill={W} />
          <circle cx={74} cy={97} r={8} fill="rgba(0,0,0,0.3)" />
          <circle cx={100} cy={97} r={8} fill="rgba(0,0,0,0.3)" />
          <circle cx={126} cy={97} r={8} fill="rgba(0,0,0,0.3)" />
        </g>
      );
    case 'warn':
      return (
        <g>
          <path d="M100 44l60 106H40z" fill={W} strokeLinejoin="round" stroke={W} strokeWidth={10} />
          <path d="M100 82v34" stroke="#5a4400" strokeWidth={12} strokeLinecap="round" />
          <circle cx={100} cy={134} r={7} fill="#5a4400" />
        </g>
      );
    case 'user':
      return (
        <g>
          <circle cx={100} cy={78} r={28} fill={W} />
          <path d="M48 156c4-30 26-46 52-46s48 16 52 46z" fill={W} />
          <circle cx={90} cy={78} r={4.5} fill="#1b3c66" />
          <circle cx={110} cy={78} r={4.5} fill="#1b3c66" />
        </g>
      );
    default:
      return null;
  }
};

/** Clay tile icon with a soft top highlight and a contact shadow. */
export const Icon: React.FC<{name: string; size: number; color?: string}> = ({name, size, color}) => {
  if (name === 'agent') return <Agent size={size} />;
  const c = color || TILE[name] || C.cyan;
  const id = `g-${name}-${c.replace('#', '')}`;
  return (
    <svg width={size} height={size} viewBox="0 0 200 200" style={{overflow: 'visible'}}>
      <defs>
        <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={c} />
          <stop offset="1" stopColor={c} stopOpacity={0.62} />
        </linearGradient>
      </defs>
      <ellipse cx={100} cy={190} rx={70} ry={10} fill="rgba(0,0,0,0.45)" />
      <rect x={10} y={10} width={180} height={172} rx={52} fill={id ? `url(#${id})` : c} />
      <rect x={10} y={10} width={180} height={172} rx={52} fill="none" stroke="rgba(255,255,255,0.35)" strokeWidth={3} />
      <path d="M40 34 Q100 18 160 34" stroke="rgba(255,255,255,0.45)" strokeWidth={10} fill="none" strokeLinecap="round" />
      <g transform="translate(0 -6)">{glyph(name)}</g>
    </svg>
  );
};

/** The channel's agent character: a friendly robot head. mood: calm | scan | evil. */
export const Agent: React.FC<{size: number; mood?: 'calm' | 'scan' | 'evil'; look?: number}> = ({size, mood = 'calm', look = 0}) => {
  const frame = useCurrentFrame();
  const blink = frame % 70 > 64 ? 0.15 : 1;
  const evil = mood === 'evil';
  const eye = evil ? C.hot : C.cyan;
  const lx = look * 10;
  const jitter = evil ? Math.sin(frame * 2.3) * 2 : 0;
  return (
    <svg width={size} height={size} viewBox="0 0 200 200" style={{overflow: 'visible'}}>
      <defs>
        <linearGradient id="agentBody" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#EAF6FF" />
          <stop offset="1" stopColor="#9FB4D8" />
        </linearGradient>
        <radialGradient id="agentGlow">
          <stop offset="0" stopColor={eye} stopOpacity={0.9} />
          <stop offset="1" stopColor={eye} stopOpacity={0} />
        </radialGradient>
      </defs>
      <ellipse cx={100} cy={192} rx={66} ry={9} fill="rgba(0,0,0,0.45)" />
      <line x1={100} y1={30} x2={100} y2={8} stroke="#9FB4D8" strokeWidth={8} strokeLinecap="round" />
      <circle cx={100} cy={8} r={10} fill={eye} opacity={0.7 + 0.3 * Math.sin(frame / 5)} />
      <rect x={22} y={30} width={156} height={150} rx={50} fill="url(#agentBody)" />
      <rect x={22} y={30} width={156} height={150} rx={50} fill="none" stroke="rgba(255,255,255,0.8)" strokeWidth={3} />
      <rect x={40} y={62} width={120} height={78} rx={30} fill="#0B1226" />
      <g transform={`translate(${lx + jitter} 0)`}>
        <circle cx={76} cy={101} r={26} fill="url(#agentGlow)" opacity={0.6} />
        <circle cx={124} cy={101} r={26} fill="url(#agentGlow)" opacity={0.6} />
        {evil ? (
          <>
            <path d="M60 92l32 10-32 8z" fill={eye} />
            <path d="M140 92l-32 10 32 8z" fill={eye} />
          </>
        ) : (
          <>
            <ellipse cx={76} cy={101} rx={11} ry={15 * blink} fill={eye} />
            <ellipse cx={124} cy={101} rx={11} ry={15 * blink} fill={eye} />
          </>
        )}
      </g>
      <path d={evil ? 'M80 158 Q100 148 120 158' : 'M82 152 Q100 164 118 152'} stroke="#41557F" strokeWidth={7} fill="none" strokeLinecap="round" />
      <circle cx={30} cy={110} r={10} fill="#9FB4D8" />
      <circle cx={170} cy={110} r={10} fill="#9FB4D8" />
    </svg>
  );
};
