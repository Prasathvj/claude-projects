// The edit: one `beat` plate per narration line. Each cut sits in the pause before its line
// (`cut`, written by tools/motion_export.py), so the picture changes on the voice's beat.
import type { TimelineEntry } from './engine/engine';
import type { SceneClass } from './engine/scene';
import type { Lyrics } from './engine/lyrics';
import type { AudioData } from './engine/audio';

const modules = import.meta.glob<{ default: SceneClass }>('./scenes/*.ts');
const scene = (name: string) => () => {
  const m = modules[`./scenes/${name}.ts`];
  return m ? m() : Promise.reject(new Error(`scene module not found: scenes/${name}.ts`));
};

export function makeTimeline(ly: Lyrics, au: AudioData): TimelineEntry[] {
  const cuts = ly.lines.map((l: any, i) => (i === 0 ? 0 : (l.cut ?? l.start - 0.12)));
  return ly.lines.map((l: any, i) => ({
    id: `b${String(i).padStart(3, '0')}`,
    load: scene('beat'),
    start: cuts[i]!,
    end: i + 1 < cuts.length ? cuts[i + 1]! : au.duration,
    params: { i },
  }));
}
