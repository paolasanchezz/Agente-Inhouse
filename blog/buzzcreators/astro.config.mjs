// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Site canônico. Em staging (Vercel genérico) usa o fallback; em produção o
// deploy define PUBLIC_SITE_URL=https://blog.buzzcreators.com.br antes do build.
const SITE = process.env.PUBLIC_SITE_URL || 'https://buzzcreators-blog.vercel.app';

// https://astro.build/config
export default defineConfig({
  site: SITE,
  trailingSlash: 'never',
  integrations: [
    sitemap({
      // não listar a página 404 no sitemap
      filter: (page) => !page.includes('/404'),
    }),
  ],
});
