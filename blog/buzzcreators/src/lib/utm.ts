import { BRAND_HOME } from '../consts';

/**
 * REGRA — links de conversão comercial (OBRIGATÓRIA).
 *
 * Todo link que leve o leitor a uma página EXTERNA da Buzzcreators para
 * conhecer/converter (ex.: "Conhecer a plataforma", link do site no rodapé e na
 * página Sobre, CTA de post para módulo/LP) DEVE carregar:
 *   - utm_source=blog
 *   - utm_content=<nome-do-artigo> — o slug do post exibido na página; nas
 *     páginas sem artigo, o identificador da página (home, tag-x, categoria-x, sobre)
 *
 * Monte SEMPRE esses links com conversionUrl(). Nunca escreva UTM à mão numa
 * string — a regra fica num lugar só e não há como esquecer um parâmetro.
 */
export function conversionUrl(
  path: string,
  utmContent: string,
  utmCampaign = 'blog'
): string {
  const url = new URL(path, BRAND_HOME);
  url.searchParams.set('utm_source', 'blog');
  url.searchParams.set('utm_medium', 'blog');
  url.searchParams.set('utm_campaign', utmCampaign);
  url.searchParams.set('utm_content', utmContent);
  return url.toString();
}

/**
 * Deriva o utm_content a partir do caminho atual (Astro.url.pathname): em posts,
 * o slug do artigo exibido; nas demais páginas, um identificador estável.
 */
export function utmContentFromPath(pathname: string): string {
  const clean = pathname.replace(/\/+$/, '');
  const post = clean.match(/^\/blog\/(.+)$/);
  if (post) return post[1];
  if (clean === '') return 'home';
  return clean.replace(/^\//, '').replace(/\//g, '-');
}
