// Constantes globais do blog. Texto e identidade centralizados aqui.

export const SITE_TITLE = 'Blog Buzzcreators';
export const SITE_DESCRIPTION =
  'Ideias práticas sobre marketing de influência, creator economy e ROI de campanhas com criadores, direto do time da Buzzcreators.';
export const SITE_TAGLINE = 'Media & Influencer Marketing';

// Marca
export const ORG_NAME = 'Buzzcreators';
export const BRAND_HOME = 'https://buzzcreators.com.br';
export const CONTACT_EMAIL = 'comercial@buzzcreators.com.br';

// --- Links de saída para o site: SEMPRE com UTM (atribuição no CRM/GA) --------
// Fonte fixa `blog-buzzcreators`; convenção alinhada a landing-pages/catalogo/lps-buzzcreators.md.
// Editar aqui num lugar só — Header/Footer/Sobre importam destas constantes.
// CTA principal ("Conhecer a plataforma") vai direto à página de Marcas (conversão), nunca à Home.
export const PLATFORM_CTA_URL =
  `${BRAND_HOME}/marcas?utm_source=blog-buzzcreators&utm_medium=blog&utm_campaign=marcas&utm_content=header-cta`;
// Links institucionais (rodapé e página Sobre) — exibem o domínio, então apontam à raiz, também com UTM.
export const SITE_URL_FOOTER =
  `${BRAND_HOME}/?utm_source=blog-buzzcreators&utm_medium=blog&utm_campaign=institucional&utm_content=footer`;
export const SITE_URL_SOBRE =
  `${BRAND_HOME}/?utm_source=blog-buzzcreators&utm_medium=blog&utm_campaign=institucional&utm_content=sobre`;

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
