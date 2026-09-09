/**
 * Recibe los envios del formulario BANT y los agrega como filas en la planilla.
 *
 * Planilla destino:
 * https://docs.google.com/spreadsheets/d/1HFdB7A0l7Pr60lpTFjEmTU63agOY2UUJrhFR2-T-rUc/edit
 *
 * PRIMERA VEZ (desde la cuenta dueña de la planilla):
 *   1. Planilla > Extensiones > Apps Script.
 *   2. Pegar este archivo completo en Codigo.gs y guardar.
 *   3. Ejecutar la funcion `prepararEncabezados` y aceptar los permisos.
 *   4. Implementar > Nueva implementacion > "Aplicacion web".
 *        - Ejecutar como: Yo
 *        - Quien tiene acceso: Cualquier usuario
 *   5. Pegar la URL /exec en la constante ENDPOINT de index.html.
 *
 * SI YA ESTABA PUBLICADO Y CAMBIAS ESTE CODIGO:
 *   Guardar NO alcanza. Hay que ir a Implementar > Administrar implementaciones,
 *   editar la implementacion activa (lapiz) y elegir Version: "Nueva version".
 *   La URL /exec no cambia, pero recien ahi empieza a correr el codigo nuevo.
 */

var ID_PLANILLA = '1HFdB7A0l7Pr60lpTFjEmTU63agOY2UUJrhFR2-T-rUc';
var NOMBRE_HOJA = 'Hoja 1'; // cambiar si la pestana destino tiene otro nombre

/**
 * Los intereses tienen una columna cada uno, marcada con "x".
 * La PRIMERA cadena de cada par es la etiqueta exacta que manda el formulario
 * (tiene que coincidir carácter por carácter con index.html). La SEGUNDA es el
 * encabezado corto que se ve en la planilla: se puede cambiar libremente sin
 * tocar la pagina. Al agregar un interes, agregalo en los dos lados y volve a
 * correr `prepararEncabezados`.
 */
var INTERESES = [
  // [ etiqueta que manda el formulario , encabezado corto en la planilla ]
  ['Monitoreo + Dashboards', 'Int · Monitoreo'],
  ['Atención + Dashboards',  'Int · Atención'],
  ['Tickets para Atención',  'Int · Tickets'],
  ['Chatbots',               'Int · Chatbots'],
  ['AI Insights',            'Int · AI Insights'],
  ['Buzz Pills',             'Int · Buzz Pills'],
  ['MCP',                    'Int · MCP'],
  ['Buzzmonitor Trends',     'Int · Trends'],
  ['Analytics',              'Int · Analytics'],
  ['Programación',           'Int · Programación'],
  ['Influenciadores',        'Int · Influenciadores'],
  ['Visual Listening',       'Int · Visual Listening'],
  ['API de Integración',     'Int · API'],
  ['Otros',                  'Int · Otros']
];

function etiquetasInteres_() { return INTERESES.map(function (p) { return p[0]; }); }
function encabezadosInteres_() { return INTERESES.map(function (p) { return p[1]; }); }

/** Ficha del lead. Las columnas de interes van despues, a la derecha. */
var COLUMNAS_FICHA = [
  'Fecha y hora',
  'Evento',
  'Correo del acuerdo',
  'Closer',
  'Intereses',
  'Situacion actual',
  'Plataforma actual',
  'Momento del proyecto',
  'Temperatura',
  'Insights'
];

function columnas_() {
  return COLUMNAS_FICHA.concat(encabezadosInteres_());
}

function hoja_() {
  var libro = SpreadsheetApp.openById(ID_PLANILLA);
  var h = libro.getSheetByName(NOMBRE_HOJA);
  if (!h) h = libro.getSheets()[0];
  return h;
}

/**
 * Escribe (o reescribe) la fila de encabezados. Solo toca la fila 1.
 * Correr despues de cambiar la lista INTERESES.
 */
function prepararEncabezados() {
  var h = hoja_();
  var cols = columnas_();
  var nFicha = COLUMNAS_FICHA.length;
  var nInt = INTERESES.length;

  h.getRange(1, 1, 1, cols.length).setValues([cols]).setFontWeight('bold');
  h.setFrozenRows(1);

  // La ficha se congela para que al desplazarte a la derecha sigas viendo
  // de quien es la fila.
  h.setFrozenColumns(4);

  // El bloque de intereses: encabezado vertical y columna angosta, para que
  // los 14 quepan en una pantalla. El contenido es solo una "x".
  var enc = h.getRange(1, nFicha + 1, 1, nInt);
  enc.setTextRotation(90).setBackground('#FFE2CC').setHorizontalAlignment('center');
  for (var i = 0; i < nInt; i++) h.setColumnWidth(nFicha + 1 + i, 38);
  h.getRange(2, nFicha + 1, Math.max(h.getMaxRows() - 1, 1), nInt)
    .setHorizontalAlignment('center');

  return 'Listo: ' + cols.length + ' columnas (' + nFicha + ' de ficha + ' + nInt + ' de interes)';
}

function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return responder_({ ok: false, error: 'Sin cuerpo en la peticion' });
    }

    var d = JSON.parse(e.postData.contents);
    var h = hoja_();
    if (h.getLastRow() === 0) prepararEncabezados();

    // Acepta arreglo (formato actual) o texto separado por " · " (formato viejo).
    var elegidos = Array.isArray(d.intereses)
      ? d.intereses
      : String(d.intereses || '').split(' · ').filter(String);

    var marcas = etiquetasInteres_().map(function (nombre) {
      return elegidos.indexOf(nombre) >= 0 ? 'x' : '';
    });

    var fila = [
      new Date(),
      d.evento || '',
      d.correo || '',
      d.closer || '',
      elegidos.join(' · '),
      d.situacion || '',
      d.plataforma || '',
      d.momento || '',
      d.temperatura || '',
      d.insights || ''
    ].concat(marcas);

    h.appendRow(fila);

    // Avisa si llego un interes que no esta en la lista: no se pierde (queda en
    // la columna resumen) pero no tiene columna propia.
    var huerfanos = elegidos.filter(function (n) { return etiquetasInteres_().indexOf(n) < 0; });

    return responder_({ ok: true, sinColumna: huerfanos });
  } catch (err) {
    return responder_({ ok: false, error: String(err) });
  }
}

/**
 * Comprobacion de vida. Devuelve solo conteos, nunca contenido de la planilla:
 * la URL es publica y no debe exponer datos de los leads.
 */
function doGet() {
  var h = hoja_();
  return responder_({
    ok: true,
    servicio: 'BANT America Digital',
    hoja: h.getName(),
    columnas: columnas_().length,
    filas: Math.max(0, h.getLastRow() - 1)
  });
}

function responder_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
