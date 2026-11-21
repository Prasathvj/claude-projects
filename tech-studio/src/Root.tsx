import React from 'react';
import {Composition, AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig} from 'remotion';
const Test: React.FC = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const n = Math.round(interpolate(f, [0, 45], [0, 133], {extrapolateRight: 'clamp'}));
  const s = spring({frame: f, fps, config: {damping: 10}});
  return (<AbsoluteFill style={{background: '#0B1226', justifyContent: 'center', alignItems: 'center'}}>
    <div style={{fontFamily: 'sans-serif', fontWeight: 900, fontSize: 260, color: '#2EE6FF', transform: `scale(${s})`}}>{n}</div>
  </AbsoluteFill>);
};
export const Root: React.FC = () => <Composition id="Test" component={Test} durationInFrames={60} fps={30} width={1080} height={1920} />;
