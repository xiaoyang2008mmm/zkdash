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
        if (nodes.length == 0) {
            alert("请先选择一个节点");
            return;
        } else {
            post_func(get_node_tree());
            for (var i = 0,
            l = nodes.length; i < l; i++) {
                treeObj.removeNode(nodes[i]);
            }
        }

    });
    //////////////////////
    function post_func(node) {
        var msg = "确定要删除吗?";
        if (confirm(msg) == true) {
            $.post("/post_delete/", {
                node_key: node,
            },
            function(data) {
                alert(data);
            });
        } else {
            return false;
        }
    }

    ////////////////////////
    $("#value_info").click(function() {
        var value_data = get_node_tree();
        if (value_data == "/") {
            alert("根节点下无数据");
        } else {
            $.post("/get_node_value/", {
                choose_node: value_data,
            },
            function(data) {
                alert(data);

            });
        };
    });

    /////////////////////////////////////////
    function get_node_tree() {
        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getSelectedNodes();
        treeNode = nodes[0];
        var value_data = treeNode.name;

        if (value_data.indexOf("/") != 0) {

            var sNodes = treeObj.getSelectedNodes();
            if (sNodes.length > 0) {
                var node = sNodes[0].getParentNode();
                console.log(node.name);
                console.log(value_data);
                if (node.name == "/") {
                    var value_data = '/' + value_data;
                } else {
                    var value_data = node.name + '/' + value_data;
                }
            }
        }
        return value_data
    }
    ////////////////////////////////////////////
    $("#value_change").click(function() {

        var value_data = get_node_tree();
        if (value_data == "/") {
            alert("根节点不能修改");
        } else {

            $.post("/get_node_value/", {
                choose_node: value_data,
            },
            function(data) {
                $('#node_name').attr("value", get_node_tree());
                $('#node_value').attr("value", data);
                $('#myModal').modal('show');

            });

        };
    });
    ////////////////////////////////////////////
    $("#commit_btn").click(function() {
        var node_name = $('#node_name').attr("value");
        var node_value = $('#node_value').val();

        $.post("/mod_node_value/", {
            node_name: node_name,
            node_value: node_value,
        },
        function(data) {
            alert(data);
            $('#myModal').modal('hide');
        });

    });

});
