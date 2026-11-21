import React from 'react';
import {Composition} from 'remotion';
import {Episode, Timeline} from './lib/Episode';
import {TIMELINES} from './episodes';
import {Thumbnail} from './lib/Thumbnail';

const size = (tl: Timeline) => (tl.format === 'vertical' ? {width: 1080, height: 1920} : {width: 1920, height: 1080});

export const Root: React.FC = () => (
  <>
    {TIMELINES.map((tl) => (
      <Composition key={tl.id} id={tl.id} component={Episode as any} defaultProps={{tl}} fps={tl.fps}
        durationInFrames={Math.ceil(tl.duration * tl.fps)} {...size(tl)} />
    ))}
    <Composition id="Thumb-ep01" component={Thumbnail as any} defaultProps={{hook: 'AGENT HIJACKED', tag: 'PROMPT INJECTION'}}
      fps={30} durationInFrames={30} width={1280} height={720} />
  </>
);
