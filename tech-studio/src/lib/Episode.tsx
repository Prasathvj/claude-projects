import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, F, STAGGER} from './theme';
import {Bg, LabelChip, PunchZoom, Rip, Sfx, useLayout, Whip} from './motion';
import {Captions} from './widgets';
import {SCENES} from './scenes';

export type Beat = {
  text: string; v: any; trans?: 'rip' | 'whip' | 'punch'; sfx?: string[];
  start: number; dur: number; vo: number; words: {w: string; s: number; e: number}[];
};
export type Timeline = {id: string; format: string; captions: string; fps: number; duration: number; vo: string; music: string; beats: Beat[]};

// Scenes that already play their own sounds for these names.
const SELF_SFX: Record<string, string[]> = {counter: ['tick', 'impact'], receipt: ['print', 'click', 'impact']};
const HOT = ['injection', 'stranger', 'hidden', 'zero', 'critical', 'danger', 'steal', 'attacker', "attacker's", 'hijack', 'never', 'scary',
  'poison', 'memory', 'solved', 'leaking', 'leak', 'malware', 'once', 'creepy'];

/** Frame offsets for a beat's sound list, matched to when each scene animates. */
const cues = (b: Beat, frames: number): [string, number][] => {
  const list = (b.sfx || []).filter((n) => !(SELF_SFX[b.v.type] || []).includes(n));
  const t = b.v.type;
  return list.map((n, i) => {
    if (t === 'browser' && b.v.reveal) return [n, Math.round(frames * 0.3) + i * 6];
    if (t === 'email' && i > 0) return [n, Math.round(frames * 0.45)];
    if (t === 'agent' && b.v.mode === 'hijack') return [n, i * 8];
    if (t === 'trifecta' && b.v.cut !== undefined) return [n, 8 + i * 8];
    if (t === 'split' && b.v.merge && i > 0) return [n, Math.round(frames * 0.5)];
    if (t === 'ruleoftwo') return [n, i < 2 ? 6 + i * STAGGER : Math.round(frames * 0.6)];
    if (t === 'flow') return [n, i * STAGGER * 1.4];
    if (t === 'tease') return [n, i * 8];
    if (t === 'chapter') return [n, i * 3];
    if (t === 'chat') return [n, 4 + i * 14];
    return [n, i * STAGGER];
  });
};

const BeatView: React.FC<{b: Beat}> = ({b}) => {
  const {durationInFrames} = useVideoConfig();
  const Scene = SCENES[b.v.type];
  const body = Scene ? <Scene {...b.v} /> : <div style={{color: C.hot, fontSize: 60}}>Unknown scene {b.v.type}</div>;
  const kick = b.trans === 'punch' ? 0.28 : 0.07;
  let content = <PunchZoom kick={kick}>{body}</PunchZoom>;
  if (b.trans === 'whip') content = <Whip>{content}</Whip>;
  return (
    <AbsoluteFill>
      {content}
      {b.v.label && b.v.type !== 'counter' && <LabelChip text={b.v.label} />}
      {b.trans === 'rip' && <Rip />}
      {b.trans === 'whip' && <Sfx name="whoosh" volume={0.7} />}
      {cues(b, durationInFrames).map(([n, at], i) => <Sfx key={i} name={n} at={at} volume={0.75} />)}
    </AbsoluteFill>
  );
};

const Brand: React.FC = () => {
  const {u, isV} = useLayout();
  return (
    <div style={{position: 'absolute', top: (isV ? 80 : 34) * u, right: 40 * u, fontFamily: F.display, fontWeight: 900, fontSize: 28 * u,
      color: C.white, opacity: 0.75, letterSpacing: 3 * u, display: 'flex', alignItems: 'center', gap: 10 * u}}>
      <div style={{width: 16 * u, height: 16 * u, borderRadius: 99, background: C.cyan, boxShadow: `0 0 ${14 * u}px ${C.cyan}`}} />
      STICK DUDE
    </div>
  );
};

const CaptionLayer: React.FC<{tl: Timeline}> = ({tl}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const b = tl.beats.find((x) => t >= x.start && t < x.start + x.dur);
  if (!b) return null;
  return <Captions words={b.words} t={t - b.start} big={tl.captions === 'big'} hot={HOT} />;
};

/** Short progress bar so viewers see the payoff is close. */
const Progress: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const {u, w} = useLayout();
  return <div style={{position: 'absolute', left: 0, bottom: 0, height: 10 * u, width: (frame / durationInFrames) * w, background: C.cyan}} />;
};

export const Episode: React.FC<{tl: Timeline}> = ({tl}) => {
  const {fps} = useVideoConfig();
  const isShort = tl.format === 'vertical';
  return (
    <AbsoluteFill style={{background: C.navy}}>
      <Bg />
      {tl.beats.map((b, i) => (
        <Sequence key={i} from={Math.round(b.start * fps) - (i === 0 ? Math.round(b.start * fps) : 0)}
          durationInFrames={Math.round((b.start + b.dur) * fps) - Math.round(b.start * fps) + (i === 0 ? Math.round(b.start * fps) : 0)}>
          <BeatView b={b} />
        </Sequence>
      ))}
      <CaptionLayer tl={tl} />
      <Brand />
      {isShort && <Progress />}
      <Audio src={staticFile(tl.vo)} />
      <Audio src={staticFile(tl.music)} volume={isShort ? 0.16 : 0.11} />
    </AbsoluteFill>
  );
};
