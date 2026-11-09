// Showcase site for amitkarpe/video-demo (Astro + Starlight). Pages are built from src/data/videos.json;
// only entries with public: true are built. Videos stream from the public GitHub Release assets (no MP4 in Git or Pages).
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import data from './src/data/videos.json' with { type: 'json' };

const pub = data.videos.filter((v) => v.public && v.mp4);
const sidebar = [
  { label: 'Home', link: '/' },
  { label: 'All videos', link: '/all/' },
  { label: 'Lineage', link: '/lineage/' },
  ...data.families
    .map((f) => ({
      label: f.name,
      collapsed: false,
      items: pub
        .filter((v) => v.family === f.id)
        .sort((a, b) => (b.order ?? 0) - (a.order ?? 0))
        .map((v) => ({
          label: v.short ?? v.title,
          link: `/videos/${v.slug}/`,
          ...(v.current ? { badge: { text: 'current', variant: 'success' } } : {}),
        })),
    }))
    .filter((g) => g.items.length),
];

export default defineConfig({
  site: 'https://amitkarpe.github.io',
  base: '/video-demo',
  integrations: [
    starlight({
      title: 'Video Showcase',
      description: 'Narrated, animated films that explain the engineering work: AWS Factory, AWSOps, Nextflow Offline and Agentic Pentest.',
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/amitkarpe/video-demo' }],
      customCss: ['./src/styles/custom.css'],
      sidebar,
      lastUpdated: false,
      pagination: false,
      head: [{ tag: 'meta', attrs: { name: 'referrer', content: 'no-referrer-when-downgrade' } }],
    }),
  ],
});
