// Prepara assets estáticos do blog:
//  1) copia os logos da marca (PNG seguros) para public/assets
//  2) gera o og-default.png (1200x630) — gradiente da marca + logo sobre card branco
// Sem dependência de fontes: usa só formas SVG + composição de PNG (robusto no Windows).
import sharp from 'sharp';
import { mkdirSync, copyFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const projectRoot = join(__dirname, '..');
const repoRoot = join(projectRoot, '..', '..');
const brandLogos = join(repoRoot, 'brand', 'buzzcreators', 'assets', 'logos');
const publicAssets = join(projectRoot, 'public', 'assets');

mkdirSync(publicAssets, { recursive: true });

// 1) Copiar logos seguros (PNG — evita o bug de serifa dos SVG com <text> vivo)
for (const file of ['logo-color.png', 'logo-icon.png']) {
  const src = join(brandLogos, file);
  if (existsSync(src)) {
    copyFileSync(src, join(publicAssets, file));
    console.log('copiado:', file);
  } else {
    console.warn('AVISO: logo não encontrado:', src);
  }
}

// 2) Gerar og-default.png
const W = 1200;
const H = 630;
const svg = `
<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3a1652"/>
      <stop offset="42%" stop-color="#6a3895"/>
      <stop offset="82%" stop-color="#ff8119"/>
      <stop offset="100%" stop-color="#ff7300"/>
    </linearGradient>
  </defs>
  <rect width="${W}" height="${H}" fill="url(#g)"/>
  <g fill="#ffffff" opacity="0.10">
    <circle cx="1040" cy="120" r="130"/>
    <circle cx="150" cy="540" r="90"/>
    <rect x="930" y="430" width="240" height="150" rx="36"/>
  </g>
  <rect x="290" y="208" width="620" height="214" rx="28" fill="#ffffff"/>
</svg>`;

const logoBuf = await sharp(join(brandLogos, 'logo-color.png'))
  .resize({ width: 470 })
  .toBuffer();
const logoMeta = await sharp(logoBuf).metadata();

const base = await sharp(Buffer.from(svg)).png().toBuffer();
await sharp(base)
  .composite([
    {
      input: logoBuf,
      left: Math.round((W - (logoMeta.width ?? 470)) / 2),
      top: Math.round(315 - (logoMeta.height ?? 66) / 2),
    },
  ])
  .png()
  .toFile(join(publicAssets, 'og-default.png'));

console.log('OG gerado: public/assets/og-default.png');
