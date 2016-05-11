var setting = {};

$(document).ready(function() {
    $.get("/keyjson/",function(data,status){
    $.fn.zTree.init($("#treeDemo"), setting, JSON.parse(data));
    alert("Data: " + typeof(JSON.parse(data)) +typeof(zNodes)+ "nStatus: " + status);
  });
});
