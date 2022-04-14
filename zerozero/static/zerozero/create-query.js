function buildQuery() {
  var query = {};

  var fields = editor["fields"].getValue();
  if (fields) {
    query['fields'] = loadYaml(fields);
  }

  var order = editor["order"].getValue();
  if (order) {
    query['order'] = loadYaml(order);
  }

  var where = editor["where"].getValue();
  if (where) {
    query['where'] = loadYaml(where);
  }

  return encodeURI(JSON.stringify(query));
}

function loadYaml(string){
  return jsyaml.load(string, indent=4);
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
    extraKeys: {
      "Tab": function(cm){
        cm.replaceSelection("   " , "end");
      }
    }
  }
  editor["where"] = CodeMirror.fromTextArea($("textarea[name=where]")[0], config);
  editor["fields"] = CodeMirror.fromTextArea($("textarea[name=fields]")[0], config);
  editor["order"] = CodeMirror.fromTextArea($("textarea[name=order]")[0], config);
});
