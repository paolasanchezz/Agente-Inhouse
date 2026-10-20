// Chamada de LLM com saida JSON garantida por schema. Tenta OpenAI e depois Anthropic (o que estiver configurado
// e funcionando), pelo mesmo motivo da api/radar.js: nao depender de um unico provedor no dia do evento.

const { fetchWithTimeout } = require('./trends');

const OPENAI_URL = 'https://api.openai.com/v1/chat/completions';
const ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_VERSION = '2023-06-01';

async function viaOpenAI({ system, user, schema, schemaName, maxTokens, timeoutMs, temperature, modelo }) {
  const resp = await fetchWithTimeout(OPENAI_URL, {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: modelo || process.env.OPENAI_MODEL || 'gpt-4o-mini',
      messages: [{ role: 'system', content: system }, { role: 'user', content: typeof user === 'string' ? user : JSON.stringify(user) }],
      response_format: { type: 'json_schema', json_schema: { name: schemaName, strict: true, schema } },
      temperature,
      max_tokens: maxTokens,
    }),
  }, timeoutMs);
  if (!resp.ok) throw new Error(`openai_${resp.status}: ${await resp.text().catch(() => '')}`);
  const data = await resp.json();
  return JSON.parse(data.choices[0].message.content);
}

async function viaAnthropic({ system, user, schema, schemaName, maxTokens, timeoutMs }) {
  const resp = await fetchWithTimeout(ANTHROPIC_URL, {
    method: 'POST',
    headers: { 'x-api-key': process.env.ANTHROPIC_API_KEY, 'anthropic-version': ANTHROPIC_VERSION, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: process.env.ANTHROPIC_MODEL || 'claude-sonnet-5',
      max_tokens: maxTokens,
      system,
      messages: [{ role: 'user', content: typeof user === 'string' ? user : JSON.stringify(user) }],
      tools: [{ name: schemaName, description: 'Devolve a resposta estruturada.', input_schema: schema }],
      tool_choice: { type: 'tool', name: schemaName },
    }),
  }, timeoutMs);
  if (!resp.ok) throw new Error(`anthropic_${resp.status}: ${await resp.text().catch(() => '')}`);
  const data = await resp.json();
  const toolUse = (data.content || []).find((b) => b.type === 'tool_use');
  if (!toolUse) throw new Error('anthropic_no_tool_use');
  return toolUse.input;
}

// Devolve o objeto JSON ou null se nenhum provedor estiver configurado/funcionando.
// modeloOpenAI: modelo mais forte para tarefas de texto/analise (se nao existir na conta ou falhar, cai no modelo padrao).
async function chamarJSON({ system, user, schema, schemaName, maxTokens = 900, timeoutMs = 20000, temperature = 0.4, modeloOpenAI = null }) {
  const args = { system, user, schema, schemaName, maxTokens, timeoutMs, temperature };
  const tentativas = [
    process.env.OPENAI_API_KEY && modeloOpenAI && { etiqueta: `openai:${modeloOpenAI}`, fn: () => viaOpenAI({ ...args, modelo: modeloOpenAI }) },
    process.env.OPENAI_API_KEY && { etiqueta: `openai:${process.env.OPENAI_MODEL || 'gpt-4o-mini'}`, fn: () => viaOpenAI(args) },
    process.env.ANTHROPIC_API_KEY && { etiqueta: `anthropic:${process.env.ANTHROPIC_MODEL || 'claude-sonnet-5'}`, fn: () => viaAnthropic(args) },
  ].filter(Boolean);
  // A funcao inteira tem 60s: o modelo forte usa o prazo cheio, e as reservas (modelo padrao, outro provedor) so 15s cada.
  for (let i = 0; i < tentativas.length; i++) {
    const tentar = tentativas[i].fn;
    args.timeoutMs = i === 0 ? timeoutMs : Math.min(timeoutMs, 15000);
    try {
      const resultado = await tentar();
      // qual modelo respondeu (nao entra no JSON: so a analise le, para o meta)
      Object.defineProperty(resultado, '_modelo', { value: tentativas[i].etiqueta, enumerable: false });
      return resultado;
    } catch (err) {
      console.error(`[buzz-radar-totem] provedor de IA falhou (${schemaName}), tentando o proximo`, err.message || err);
    }
  }
  return null;
}

module.exports = { chamarJSON };
