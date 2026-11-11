// Paises que o visitante pode escolher no totem LATAM (parametro `p` da URL de analise, codigo ISO de 2 letras).
// A Trends guest NAO filtra post por pais (testado em 2026-11-10: `location`, `country` e `countries` sao ignorados e
// ~90% dos posts nao trazem a localizacao do autor). O pais segmenta a analise por outros caminhos:
//   - a IA monta as buscas para o mercado daquele pais (concorrentes locais, @perfil e #hashtag locais, vocabulario da categoria);
//   - os perfis ligados a marca vem filtrados por pais (a busca de influenciadores aceita `countries` com o codigo ISO);
//   - as series diarias usam o fuso do pais.
// Sem pais (links antigos), vale o comportamento anterior: Mexico como referencia.

const PAISES = {
  MX: { codigo: 'MX', nome: 'México', zona: 'America/Mexico_City' },
  CO: { codigo: 'CO', nome: 'Colombia', zona: 'America/Bogota' },
  CL: { codigo: 'CL', nome: 'Chile', zona: 'America/Santiago' },
  AR: { codigo: 'AR', nome: 'Argentina', zona: 'America/Argentina/Buenos_Aires' },
  PE: { codigo: 'PE', nome: 'Perú', zona: 'America/Lima' },
};

// "mx", " MX " -> "MX"; qualquer outro valor -> '' (sem pais).
function limparPais(valor) {
  const c = String(valor || '').trim().toUpperCase();
  return PAISES[c] ? c : '';
}

function dadosDoPais(codigo) {
  return PAISES[limparPais(codigo)] || null;
}

// Diferenca em horas do fuso do pais para UTC, agora (Chile tem horario de verao: -3 no verao, -4 no inverno).
// Sem pais, -6 (Cidade do Mexico, sem horario de verao desde 2022), como antes.
function fusoHoras(codigo, quando = new Date()) {
  const pais = dadosDoPais(codigo);
  if (!pais) return -6;
  try {
    const partes = new Intl.DateTimeFormat('en-US', { timeZone: pais.zona, timeZoneName: 'shortOffset' }).formatToParts(quando);
    const nome = (partes.find((p) => p.type === 'timeZoneName') || {}).value || '';
    const m = nome.match(/GMT([+-]\d{1,2})(?::(\d{2}))?/);
    if (!m) return 0;
    const h = Number(m[1]);
    return h + Math.sign(h) * (Number(m[2] || 0) / 60);
  } catch (err) {
    return -6;
  }
}

module.exports = { PAISES, limparPais, dadosDoPais, fusoHoras };
