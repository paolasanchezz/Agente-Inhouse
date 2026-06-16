// Builders de JSON-LD (schema.org). Centralizam a estrutura para todo post
// sair com structured data consistente — base do SEO rich results e do GEO.
import { ORG_NAME, BRAND_HOME, SITE_TITLE, SITE_DESCRIPTION, ORG_LOGO } from '../consts';

type Json = Record<string, unknown>;

export function organization(site: URL): Json {
  return {
    '@type': 'Organization',
    '@id': `${BRAND_HOME}/#organization`,
    name: ORG_NAME,
    url: BRAND_HOME,
    logo: new URL(ORG_LOGO, site).toString(),
  };
}

export function website(site: URL): Json {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: SITE_TITLE,
    description: SITE_DESCRIPTION,
    url: site.toString(),
    publisher: organization(site),
  };
}

export function blogPosting(opts: {
  title: string;
  description: string;
  url: URL;
  image: URL;
  datePublished: Date;
  dateModified?: Date;
  authorName: string;
  tags?: string[];
  site: URL;
}): Json {
  return {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: opts.title,
    description: opts.description,
    image: opts.image.toString(),
    mainEntityOfPage: { '@type': 'WebPage', '@id': opts.url.toString() },
    datePublished: opts.datePublished.toISOString(),
    dateModified: (opts.dateModified ?? opts.datePublished).toISOString(),
    author: { '@type': 'Person', name: opts.authorName },
    publisher: organization(opts.site),
    keywords: opts.tags?.join(', '),
    inLanguage: 'pt-BR',
  };
}

export function breadcrumb(items: { name: string; url: string }[]): Json {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

export function faqPage(faq: { q: string; a: string }[]): Json {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faq.map((f) => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a },
    })),
  };
}
