import {continueRender, delayRender, staticFile} from 'remotion';

export const C = {
  navy: '#0B1226',
  navy2: '#121B36',
  navy3: '#1A2547',
  line: '#26335E',
  cyan: '#2EE6FF',
  hot: '#FF4D6D',
  white: '#F4F7FF',
  dim: '#8C9AC4',
  gold: '#FFD166',
  green: '#3DDC97',
};

export const F = {
  display: 'StudioDisplay, "Inter Display", Inter, sans-serif',
  ui: 'StudioUI, Inter, sans-serif',
  mono: 'StudioMono, "JetBrains Mono", monospace',
};

// Fonts ship in public/fonts so renders look the same on any machine.
const FONTS: [string, string, string][] = [
  ['StudioDisplay', 'InterDisplay-Black.otf', '900'],
  ['StudioDisplay', 'InterDisplay-Bold.otf', '700'],
  ['StudioUI', 'Inter-SemiBold.otf', '600'],
  ['StudioUI', 'Inter-Medium.otf', '500'],
  ['StudioMono', 'JetBrainsMono-Bold.ttf', '700'],
  ['StudioMono', 'JetBrainsMono-Regular.ttf', '400'],
];

if (typeof window !== 'undefined' && typeof FontFace !== 'undefined') {
  const handle = delayRender('fonts');
  Promise.all(
    FONTS.map(([family, file, weight]) =>
      new FontFace(family, `url(${staticFile('fonts/' + file)})`, {weight}).load().then((f) => (document.fonts as any).add(f)),
    ),
  )
    .then(() => continueRender(handle))
    .catch(() => continueRender(handle));
}

/** Frames between staggered items. SFX lists use the same spacing so sounds land on the pops. */
export const STAGGER = 7;
