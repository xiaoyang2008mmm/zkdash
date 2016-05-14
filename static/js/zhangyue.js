var setting = {
    callback: {
        onClick: onClick
    }
};

function onClick(event, treeId, treeNode, clickFlag) {
    $('#zk_tree').attr("value", get_parent_tree());
    $('#zk_name').attr("value", treeNode.name);
}

function get_parent_tree() {
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
            var result = post_func(get_node_tree());
            if (String(result) != "false") {
                for (var i = 0,
                l = nodes.length; i < l; i++) {
                    treeObj.removeNode(nodes[i]);
                }
            }
        }

    });
    //////////////////////
    //需要获取函数里的函数的返回值,待改动
    function post_func(node) {
        var msg = "确定要删除吗?";
        if (confirm(msg) == true) {
            $.post("/post_delete/", {
                node_key: node,
            },
            function(data) {
                alert(data);
                if (data == "无法删除节点") {
                    return false;
                }

            });
        } else {
            return false;
        }
    }

    ////////////////////////
    $("#value_info").click(function() {


        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getSelectedNodes();
        treeNode = nodes[0];
        if (nodes.length == 0) {
            alert("请先选择一个节点");
            return;
        } else {

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
    ////////////////////////////////////////////
    $("#value_add").click(function() {
        $('#parent_node_name').attr("value", get_node_tree());
        $('#myModal_add').modal('show');
        $('#new_node_name').val("");
        $('#new_node_value').val("");
        var new_node_name = $('#new_node_name').val();
        var new_node_value = $('#new_node_value').val();
    });
    ////////////////////////////////////////////
    $("#value_post").click(function() {
        var node_name = $('#parent_node_name').attr("value");
        var new_node_name = $('#new_node_name').val();
        var new_node_value = $('#new_node_value').val();
        if (node_name != "/") {
            var New_post_node = node_name + "/" + new_node_name;
        } else {
            var New_post_node = "/" + new_node_name;

        }
        alert(New_post_node + new_node_value);
        if (new_node_name == "") {
            alert("新节点名必须增加");
        } else {
            $.post("/add_node/", {
                New_post_node: New_post_node,
                new_node_value: new_node_value,
            },
            function(data) {
                alert(data);
                $('#myModal_add').modal('hide');
                var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
                var nodes = treeObj.getSelectedNodes();
                var newNode = {
                    name: new_node_name
                };
                newNode = treeObj.addNodes(nodes[0], newNode);

            });
        }

    });
    ////////////////////////////////////////////
    $("#batch_xiugai").click(function() {
        $('#myModal_batch').modal('show');
        $('#add_node_name').attr("value", get_node_tree());
    });
    ////////////////////////////////////////////
    $("#batch_delete").click(function() {

        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var sNodes = treeObj.getSelectedNodes();
        if (sNodes.length > 0) {
            var isParent = sNodes[0].isParent;
            if (String(isParent) != "false") {
                var value_data = get_node_tree();

                var result = post_batch_delete(value_data);

                if (String(result) != "false") {
                    for (var i = 0,
                    l = sNodes.length; i < l; i++) {
                        treeObj.removeNode(sNodes[i]);
                    }
                }

            } else {
                alert("该节点为子节点,批量删除请选择父节点");
            };
        } else {
            alert("请先选择一个节点");
            return;
        };

    });
    //////////////////////
    function post_batch_delete(node) {
        var msg = "确定要删除吗?";
        if (confirm(msg) == true) {
            var res_msg = $.post("/batch_delete/", {
                node_key: node,
            },
            function(data) {
                alert(data);
            });
            return res_msg;
        } else {
            return false;
        }
    }

});
