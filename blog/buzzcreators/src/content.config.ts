import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Coleção de posts do blog. O schema é o "contrato de SEO/GEO": se um post não
// tiver os campos obrigatórios (ou fora dos limites), o `astro build` FALHA.
// Arquivos iniciados com "_" (ex.: _TEMPLATE.md) são ignorados.
const blog = defineCollection({
  loader: glob({ pattern: ['**/*.md', '!**/_*'], base: './src/content/blog' }),
  schema: z
    .object({
      // SEO — título e descrição com tamanhos amigáveis a busca/preview social
      title: z.string().min(10, 'title curto demais').max(75, 'title > 75 chars'),
      metaTitle: z.string().max(65, 'metaTitle > 65 chars').optional(),
      description: z
        .string()
        .min(110, 'meta description curta (mín. 110)')
        .max(165, 'meta description longa (máx. 165)'),

      // Datas e autoria
      pubDate: z.coerce.date(),
      updatedDate: z.coerce.date().optional(),
      author: z.string().default('Equipe Buzzcreators'),

      // Taxonomia (interlinks + páginas de tag)
      tags: z.array(z.string()).min(1, 'inclua ao menos 1 tag').max(6),
      category: z.string().optional(),

      // GEO — "Principais pontos": resumo extraível por IA (obrigatório)
      tldr: z.array(z.string()).min(2, 'inclua ao menos 2 pontos no tldr').max(6),

      // GEO — FAQ vira FAQPage schema + seção de perguntas
      faq: z
        .array(z.object({ q: z.string(), a: z.string() }))
        .default([]),

      // Imagem de capa/OG opcional (path absoluto sob /assets). Sem capa, usa o OG padrão.
      cover: z.string().startsWith('/assets/', 'cover deve apontar para /assets/...').optional(),
      coverAlt: z.string().optional(),

      draft: z.boolean().default(false),
      canonical: z.string().url().optional(),
    })
    // Acessibilidade/SEO: se tem capa, exige texto alternativo
    .refine((d) => !d.cover || (d.coverAlt && d.coverAlt.length > 0), {
      message: 'coverAlt é obrigatório quando cover é definido',
      path: ['coverAlt'],
    }),
});

export const collections = { blog };
