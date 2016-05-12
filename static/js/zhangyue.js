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
        alert("wdqwdq");

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

});
