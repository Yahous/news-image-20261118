// News image entry for 18 November 2026 (Node 22, standard library only).
// The front page in entry.png was drawn for this day's news; this program
// copies it, byte for byte, to the output directory the grader reads.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// The copy is deterministic: two runs write identical bytes.

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);
const target = join(outDir, 'entry.png');

mkdirSync(dirname(target), { recursive: true });
copyFileSync(source, target);

// Guard the gate: refuse to report success on a partial copy.
const written = readFileSync(target);
const original = readFileSync(source);
if (!written.equals(original)) {
  throw new Error('entry.png did not copy cleanly');
}
