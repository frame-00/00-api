function buildQuery() {
  var query = {};

  var fields = editor["fields"].getValue();
  if (fields) {
    query['fields'] =  jsyaml.load(fields);
  }

  var order = editor["order"].getValue();
  if (order) {
    query['order'] =  jsyaml.load(order);
  }

  var where = editor["where"].getValue();
  if (where) {
    query['where'] =  jsyaml.load(where);
  }

  return encodeURI(JSON.stringify(query));
}

function getUrl() {
  var baseUrl = `${location.protocol}//${location.host}/zerozero/api/`;
  var modelName = $("select[name=model]").val();
  var query = buildQuery();
  return `${baseUrl}${modelName}/?query=${query}&format=csv`;
}

function copyUrl() {
  navigator.clipboard.writeText(getUrl());
}

var editor = {};
$(document).ready(function () {
  var config = {
    mode: 'yaml',
    smartIndent: true,
    tabSize: 4,
    indentWithTabs: false,
    lineNumbers: false,
    theme: "duotone-light",
  }
  editor["where"] = CodeMirror.fromTextArea($("textarea[name=where]")[0], config);
  editor["fields"] = CodeMirror.fromTextArea($("textarea[name=fields]")[0], config);
  editor["order"] = CodeMirror.fromTextArea($("textarea[name=order]")[0], config);
});
