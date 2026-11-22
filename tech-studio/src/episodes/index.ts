import ep01_long from './ep01-long.timeline.json';
import ep01_short from './ep01-short.timeline.json';
import news01_short from './news01-short.timeline.json';
import news02_short from './news02-short.timeline.json';
import tip01_short from './tip01-short.timeline.json';
import type {Timeline} from '../lib/Episode';
export const TIMELINES = [ep01_long, ep01_short, news01_short, news02_short, tip01_short] as unknown as Timeline[];
