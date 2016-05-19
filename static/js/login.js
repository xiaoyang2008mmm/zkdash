$(document).ready(function() {
    function chesum_login() {

        var $login_username = $("#login_username").val();
        var $login_password = $("#login_password").val();
        $.post("/login/", {
            login_username: $login_username,
            login_password: $login_password,
        },
        function(data) {
            if (data == "ok") {
                location.href = '/zk_page/';
            } else {
                alert(data);
            }
        });

    }
    $("#login_button").click(function() {
        chesum_login();
    });

    $('#login_password').bind('keypress',
    function(event) {
        if (event.keyCode == "13") {
            chesum_login();
        }
    });

})
