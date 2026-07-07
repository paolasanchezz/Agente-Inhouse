import { getCollection } from 'astro:content';
import { slugify } from './slug';

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
    .map(([slug, { label, count }]) => ({ slug, label, count }))
    .sort((a, b) => a.label.localeCompare(b.label, 'pt-BR'));
}
