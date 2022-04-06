function convertListToArray(list) {
  return list ? list.replace(/\s*/g, '').split(',') : '';
}

function buildQuery() {
  var query = {};

  var fields = $("textarea[name=fields]").val();
  if (fields) {
    query['fields'] = convertListToArray(fields)
  }

  var order = $("textarea[name=order]").val();
  if (order) {
    query['order'] = convertListToArray(order)
  }

  var where = $("textarea[name=where]").val();
  if (where) {
    query['where'] =  jsyaml.load(where);
  }

  return encodeURI(JSON.stringify(query));
}

function getUrl(extra) {
  var baseUrl = `${location.protocol}//${location.host}/zerozero/api/`;
  var modelName = $("select[name=model]").val();
  var query = buildQuery();
  var extraFields = extra ? `&${encodeURI(extra)}` : '';

  return `${baseUrl}${modelName}/?query=${query}${extraFields}`;
}

$(document).ready(function () {
  CodeMirror.fromTextArea($("textarea[name=where]")[0], { mode: 'yaml' });
});
