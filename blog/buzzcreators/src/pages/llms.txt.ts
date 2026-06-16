import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { SITE_TITLE, SITE_DESCRIPTION, BRAND_HOME } from '../consts';

// llms.txt — índice em texto limpo do conteúdo do blog, pensado para LLMs
// (padrão emergente de GEO). Gerado a partir dos posts reais.
export const GET: APIRoute = async (context) => {
  const posts = (await getCollection('blog', ({ data }) => !data.draft)).sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );

  const lines = [
    `# ${SITE_TITLE}`,
    '',
    `> ${SITE_DESCRIPTION}`,
    '',
    `Marca: Buzzcreators (${BRAND_HOME}), plataforma de gestão de marketing de influência.`,
    '',
    '## Artigos',
    ...posts.map((p) => {
      const url = new URL(`/blog/${p.id}/`, context.site).toString();
      return `- [${p.data.title}](${url}): ${p.data.description}`;
    }),
    '',
  ];

  return new Response(lines.join('\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
