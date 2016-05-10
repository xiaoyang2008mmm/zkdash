$(document).ready(function() {
    $('body').on('click', 'button[id*=v_edit]',
    function() {
        var $this = $(this);
        var $host = $($this.parent().parent().find('strong')).text();
        var $select_index = $($this.parent().parent().find('select'));
        var $select_file = $select_index.find("option:selected").text();
        //console.log($host);
        alert($host + $select_file);
        $("#vhost_text").text('您现在修改的是IP:' + $host + '配置文件为:' + $select_file);

        if ($host == "") {
            alert("没有主机");
        } else {
            $.post("/host_vhost/", {
                host: $host,
                select_file: $select_file,
            },
            function(data) {
                alert(data);
		$("#vhost_comment").text(data);
            });
        };

    });
    ////////////////// nginx conf 语法检查
    $('body').on('click', 'button[id*=v_test]',
    function() {
        var $this = $(this);
        var $host = $($this.parent().parent().find('strong')).text();
        //console.log($host);
        alert($host);
    });
    ////////////////// 重新reload  nginx
    $('body').on('click', 'button[id*=v_reload]',
    function() {
        var $this = $(this);
        var $host = $($this.parent().parent().find('strong')).text();
        //console.log($host);
        alert($host);
    });
    ////////////////提交修改后的内容
    $("#comment_post").click(function() {
	if($("#vhost_comment").val() == "") {
	    $("#vhost_error").addClass("has-error");
	}else{
	    post_func();
	};
     });
    function post_func() {
        var msg = "确定要提交吗?";
	var $v_after =$("#vhost_comment").val();
        if (confirm(msg) == true) {
            $.post("/post_vhost/", {
                $v_after: $v_after,
            },
            function(data) {
                alert(data);
            });
	    $("#vhost_comment").val("");
        } else {
            return false;
        }
    }

});
