import { getCollection } from 'astro:content';
import { slugify } from './slug';

// Categorias com seção própria no menu principal: em vez da página genérica
// /categoria/{slug}, apontam para a página dedicada (slug da categoria -> rota).
// A /categoria/{slug} dessas não é gerada; o vercel.json redireciona (308).
export const SECTION_CATEGORIES: Record<string, string> = {
  cases: '/cases',
};

// URL da página de uma categoria (seção dedicada ou /categoria/{slug}).
export function categoryHref(label: string): string {
  const slug = slugify(label);
  return SECTION_CATEGORIES[slug] ?? `/categoria/${slug}`;
}

// Categorias únicas derivadas dos posts — fonte para a linkagem interna
// (rodapé sitewide, chips da home e páginas /categoria/[category]).
// Uma categoria por post; ordenadas alfabeticamente em pt-BR.
export async function getCategories() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const map = new Map<string, { label: string; count: number }>();
  for (const post of posts) {
    const cat = post.data.category;
    if (!cat) continue;
    const slug = slugify(cat);
    const entry = map.get(slug);
    if (entry) entry.count += 1;
    else map.set(slug, { label: cat, count: 1 });
  }
  return [...map.entries()]
    .map(([slug, { label, count }]) => ({ slug, label, count, href: categoryHref(label) }))
    .sort((a, b) => a.label.localeCompare(b.label, 'pt-BR'));
}
