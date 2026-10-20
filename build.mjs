// Prepara il sito per la pubblicazione nella cartella dist/.
// Vercel e Netlify lo eseguono da soli (vedi vercel.json e netlify.toml):
// leggono l'indirizzo del sito e completano canonical, anteprime social
// con immagine, sitemap.xml e robots.txt.
// Su un altro hosting: SITE_URL=https://tuodominio.it node build.mjs, poi carica dist/.
import { cpSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';

const raw = process.env.SITE_URL || process.env.VERCEL_PROJECT_PRODUCTION_URL || process.env.URL || '';
const base = raw ? (/^https?:\/\//.test(raw) ? raw : `https://${raw}`).replace(/\/+$/, '') + '/' : '';

rmSync('dist', { recursive: true, force: true });
mkdirSync('dist');
for (const dir of ['img', 'video']) cpSync(dir, `dist/${dir}`, { recursive: true });

let html = readFileSync('index.html', 'utf8');
let robots = 'User-agent: *\nAllow: /\n';

const swap = (from, to) => {
  if (!html.includes(from)) { console.warn('Non trovato nella pagina:', from); return; }
  html = html.replace(from, to);
};

if (base) {
  const abs = (path) => base + path;
  swap('<meta property="og:image" content="img/og-image.jpg">',
    `<link rel="canonical" href="${base}">\n` +
    `<meta property="og:url" content="${base}">\n` +
    `<meta property="og:image" content="${abs('img/og-image.jpg')}">`);
  swap('"@id": "#oleificio"', `"@id": "${base}#oleificio"`);
  swap('"url": "./"', `"url": "${base}"`);
  swap('"image": "img/og-image.jpg"', `"image": "${abs('img/og-image.jpg')}"`);
  swap('"logo": "img/logo.webp"', `"logo": "${abs('img/logo.webp')}"`);

  const today = new Date().toISOString().slice(0, 10);
  writeFileSync('dist/sitemap.xml',
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    `  <url><loc>${base}</loc><lastmod>${today}</lastmod></url>\n` +
    '</urlset>\n');
  robots += `Sitemap: ${base}sitemap.xml\n`;
  console.log('Sito pronto per', base);
} else {
  console.log('Indirizzo del sito non trovato: imposta SITE_URL per canonical, anteprime e sitemap.');
}

writeFileSync('dist/robots.txt', robots);
writeFileSync('dist/index.html', html);
