// Constantes globais do blog. Texto e identidade centralizados aqui.

export const SITE_TITLE = 'Blog Buzzcreators';
export const SITE_DESCRIPTION =
  'Ideias práticas sobre marketing de influência, creator economy e ROI de campanhas com criadores, direto do time da Buzzcreators.';
export const SITE_TAGLINE = 'Media & Influencer Marketing';

// Marca
export const ORG_NAME = 'Buzzcreators';
export const BRAND_HOME = 'https://buzzcreators.com.br';
export const CONTACT_EMAIL = 'comercial@buzzcreators.com.br';

// Assets (servidos de /public)
export const ORG_LOGO = '/assets/logo-color.png';
export const FAVICON = '/assets/logo-icon.png';
export const OG_DEFAULT = '/assets/og-default.png';

// Controle de indexação por ambiente.
// Staging (Vercel genérico): noindex ligado (default) para o Google não indexar a homologação.
// Produção: o deploy define PUBLIC_NOINDEX=false antes do build.
export const NOINDEX = (import.meta.env.PUBLIC_NOINDEX ?? 'true') !== 'false';

// Navegação principal do blog
export const NAV_LINKS = [
  { href: '/', label: 'Início' },
  { href: '/sobre', label: 'Sobre' },
];
