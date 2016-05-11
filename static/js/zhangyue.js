var setting = {};
$(document).ready(function() {

    $.get("/get_base_node/",function(data,status){
      $.fn.zTree.init($("#treeDemo"), setting, JSON.parse(data));
     //alert("Data: " + typeof(JSON.parse(data)) +typeof(zNodes)+ "nStatus: " + status);
     //alert("Data: " + typeof(JSON.parse(data)) +typeof(zNodes)+ "nStatus: " + status);
    });

////////////////////////
$("#node_search").click(function() {
    if ($("#node_path").val() == "") {
        alert("输入首节点路劲");
    } else {
        $.post("/node_path/", {
            node_path: $("#node_path").val(),
        },
        function(data) {
            $.fn.zTree.init($("#treeDemo"), setting, JSON.parse(data));

        });
    };
});
////////////////////////

});
