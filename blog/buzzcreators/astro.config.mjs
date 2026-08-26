// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Site canônico. Em staging (Vercel genérico) usa o fallback; em produção o
// deploy define PUBLIC_SITE_URL=https://blog.buzzcreators.com.br antes do build.
const SITE = process.env.PUBLIC_SITE_URL || 'https://buzzcreators-blog.vercel.app';

/**
 * Abre em nova aba todo link do corpo do post (internos e externos).
 * Roda no build, sobre o HTML já gerado do markdown — vale para todos os posts,
 * atuais e futuros, sem precisar marcar nada no .md.
 *
 * Fora do escopo de propósito: âncora interna (#...), mailto: e tel:. Nesses,
 * abrir aba nova quebra o comportamento esperado (pulo na própria página e
 * handler do sistema). Header, footer e cards de post são navegação do site,
 * não corpo do post, e seguem na mesma aba.
 *
 * rel="noopener noreferrer" acompanha target="_blank" por segurança: sem ele a
 * página de destino recebe acesso a window.opener e pode reescrever a origem.
 */
function rehypeLinksNewTab() {
  const skip = ['#', 'mailto:', 'tel:'];
  return (tree) => {
    const walk = (node) => {
      if (node.tagName === 'a' && node.properties) {
        const href = String(node.properties.href ?? '');
        if (href && !skip.some((p) => href.startsWith(p))) {
          node.properties.target = '_blank';
          node.properties.rel = 'noopener noreferrer';
        }
      }
      if (node.children) node.children.forEach(walk);
    };
    walk(tree);
  };
}

// https://astro.build/config
export default defineConfig({
  site: SITE,
  trailingSlash: 'never',
  markdown: {
    rehypePlugins: [rehypeLinksNewTab],
  },
  integrations: [
    sitemap({
      // não listar a página 404 no sitemap
      filter: (page) => !page.includes('/404'),
    }),
  ],
});
