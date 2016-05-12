var setting = {};
$(document).ready(function() {

    $.get("/get_base_node/",
    function(data, status) {
        $.fn.zTree.init($("#treeDemo"), setting, JSON.parse(data));
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
    //
    $("#delete_btn").click(function() {

        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getSelectedNodes();
        treeNode = nodes[0];
        alert(treeNode.name);
        if (nodes.length == 0) {
            alert("请先选择一个节点");
            return;
        }
        for (var i = 0,
        l = nodes.length; i < l; i++) {
            treeObj.removeNode(nodes[i]);
        }
    });
    ////////////////////////
    $("#value_info").click(function() {
	var value_data=get_node_tree();
        if (value_data == "/") {
            alert("根节点下无数据");
        } else {
            $.post("/get_node_vsalue/", {
                choose_node: value_data,
            },
            function(data) {
                alert(data);

            });
        };
    });

/////////////////////////////////////////
function get_node_tree(){
        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getSelectedNodes();
        treeNode = nodes[0];
        var value_data = treeNode.name;

        if (value_data.indexOf("/") != 0) {

            var sNodes = treeObj.getSelectedNodes();
            if (sNodes.length > 0) {
                var node = sNodes[0].getParentNode();
                var value_data = node.name + '/' + value_data;
            }
        }
	return value_data
}





});
