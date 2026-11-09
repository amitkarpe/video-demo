import data from '../data/videos.json';

export type Video = (typeof data.videos)[number] & Record<string, any>;
export const all: Video[] = data.videos as Video[];
export const videos: Video[] = all.filter((v) => v.public && v.mp4);
export const repos = data.repos as Record<string, { name: string; url: string | null; visibility: string; note?: string }>;
export const families = data.families;
export const looks = data.looks as Record<string, string>;

const BASE = import.meta.env.BASE_URL.replace(/\/$/, '');
export const url = (p: string) => `${BASE}/${p.replace(/^\//, '')}`;
export const frame = (slug: string, n = 2) => url(`frames/${slug}-${n}.jpg`);
export const familyName = (id: string) => families.find((f) => f.id === id)?.name ?? id;

export function mmss(sec?: number | null) {
  if (!sec) return '';
  const s = Math.round(sec);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
}
export function niceDate(d?: string | null) {
  if (!d) return '';
  return new Date(d + 'T12:00:00Z').toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
}
export const byNewest = (a: Video, b: Video) => (b.date ?? '').localeCompare(a.date ?? '') || (b.order ?? 0) - (a.order ?? 0);
export function series(v: Video) {
  return videos.filter((x) => x.series === v.series).sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
}
export function stats() {
  const runtime = videos.reduce((t, v) => t + (v.durationSec ?? 0), 0);
  return {
    videos: videos.length,
    madeTotal: all.filter((v) => v.durationSec && v.kind !== 'stills' && v.kind !== 'interactive').length,
    runtimeMin: Math.round(runtime / 60),
    families: new Set(videos.map((v) => v.family)).size,
    repos: new Set(videos.map((v) => v.repo).filter((r) => repos[r]?.url && r !== 'video-demo')).size,
    looks: new Set(videos.map((v) => v.look)).size,
    days: new Set(videos.map((v) => v.date)).size,
  };
}

// The film's spoken words, for the page and for search: the site's own copy (factory films), else the archived film's
// transcript.txt or captions.srt in this repository (read at build time; paths are relative to site/).
import fs from 'node:fs';
export function transcript(v: Video): string[] {
  const tryRead = (p: string) => { try { return fs.readFileSync(p, 'utf8'); } catch { return null; } };
  let t = (v.transcript && tryRead(v.transcript)) || (v.film && tryRead(`../${v.film}/transcript.txt`));
  if (!t && v.film) {
    const srt = tryRead(`../${v.film}/captions.srt`);
    if (srt) t = srt.split(/\r?\n\r?\n/).map((b) => b.split(/\r?\n/).filter((l) => l && !/^\d+$/.test(l) && !/-->/.test(l)).join(' ')).join('\n');
  }
  return (t ?? '').split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
}
