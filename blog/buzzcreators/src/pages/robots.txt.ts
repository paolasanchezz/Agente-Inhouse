import type { APIRoute } from 'astro';
import { NOINDEX } from '../consts';

// robots.txt gerado por ambiente:
// - staging (NOINDEX): bloqueia tudo (homologação não deve ser rastreada)
// - produção: libera geral + dá boas-vindas explícitas aos crawlers de IA (GEO)
export const GET: APIRoute = (context) => {
  const sitemap = new URL('/sitemap-index.xml', context.site).toString();

  const aiBots = [
    'GPTBot',
    'OAI-SearchBot',
    'ChatGPT-User',
    'ClaudeBot',
    'Claude-Web',
    'anthropic-ai',
    'PerplexityBot',
    'Perplexity-User',
    'Google-Extended',
    'Applebot-Extended',
    'CCBot',
  ];

  const body = NOINDEX
    ? `# Ambiente de homologacao (nao indexar)\nUser-agent: *\nDisallow: /\n`
    : [
        'User-agent: *',
        'Allow: /',
        '',
        '# Crawlers de IA (GEO): citacao permitida',
        ...aiBots.flatMap((bot) => [`User-agent: ${bot}`, 'Allow: /']),
        '',
        `Sitemap: ${sitemap}`,
        '',
      ].join('\n');

  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
