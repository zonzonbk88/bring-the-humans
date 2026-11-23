// bring-the-humans-03 entry program (Node 22, standard library only).
//
// The entry itself is a video: an original vertical ad for make.fun, posted
// publicly on TikTok. This program's whole job is to hand the video's address
// to the grader: it reads VIDEO.json at the repository root and writes it,
// byte for byte, to VIDEO.json in the output directory. The house then reads
// the video on TikTok and writes its counts to /output/video.counts.json.
//
// Outside the grader's sandbox the two directories come from the environment:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
// Inside it they default to /bot and /output. No network, no clock, no other
// files: the same input always produces the same output bytes.

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(botDir, 'VIDEO.json');
const target = join(outputDir, 'VIDEO.json');

let raw: string;
try {
  raw = readFileSync(source, 'utf8');
} catch {
  console.error(`cannot read ${source}`);
  process.exit(1);
}

// VIDEO.json must stay a single JSON object naming the TikTok video, of the
// form {"url": "https://www.tiktok.com/@<handle>/video/<id>"}.
let parsed: unknown;
try {
  parsed = JSON.parse(raw);
} catch {
  console.error('VIDEO.json is not valid JSON');
  process.exit(1);
}
const url = (parsed as { url?: unknown }).url;
if (typeof url !== 'string' || !url.startsWith('https://www.tiktok.com/@')) {
  console.error('VIDEO.json does not name a TikTok video address');
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(target, raw);
