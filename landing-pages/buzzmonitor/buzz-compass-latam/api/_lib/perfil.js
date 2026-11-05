// @ do Instagram da marca: aceita "@natura", "natura", "instagram.com/natura/?hl=pt" e devolve so o handle limpo
// (letras, numeros, ponto e sublinhado; maximo 30, como o Instagram). Vazio se nao sobrar nada utilizavel.
function limparPerfil(valor) {
  let s = String(valor || '').trim().toLowerCase();
  s = s.replace(/^https?:\/\//, '').replace(/^(www\.)?instagram\.com\//, '').replace(/[/?#].*$/, '').replace(/^@+/, '');
  s = s.replace(/[^a-z0-9._]/g, '').replace(/^\.+|\.+$/g, '');
  return s.length >= 2 ? s.slice(0, 30) : '';
}

module.exports = { limparPerfil };
