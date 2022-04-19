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
function yamlToJson(ev) {
  ev.preventDefault();
  editor["where"].getDoc().setValue(JSON.stringify(jsyaml.load(editor["where"].getDoc().getValue())));
  editor["fields"].getDoc().setValue(JSON.stringify(jsyaml.load(editor["fields"].getDoc().getValue())));
  editor["order"].getDoc().setValue(JSON.stringify(jsyaml.load(editor["order"].getDoc().getValue())));
  $(this).unbind();
  $(this).click();
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
  var where = $("textarea[name=where]");
  var fields = $("textarea[name=fields]");
  var order = $("textarea[name=order]");
  where.val(jsyaml.dump(JSON.parse(where.val())));
  fields.val(jsyaml.dump(JSON.parse(fields.val())));
  order.val(jsyaml.dump(JSON.parse(order.val())));
  $("button[name=save]").click(yamlToJson)
  $("button[name=save-and-download]").click(yamlToJson)
  editor["where"] = CodeMirror.fromTextArea(where[0], config);
  editor["fields"] = CodeMirror.fromTextArea(fields[0], config);
  editor["order"] = CodeMirror.fromTextArea(order[0], config);
});
