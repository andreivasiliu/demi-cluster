var id_token = null;

function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();

    id_token = googleUser.getAuthResponse().id_token;

    var p = document.getElementById("mydata");

    p.textContent = 'ID: ' + profile.getId();
    p.textContent += ', Name: ' + profile.getName();
    p.textContent += ', Image URL: ' + profile.getImageUrl();
    p.textContent += ', Email: ' + profile.getEmail();
}

function getCookie() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/get_cookie');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        var p = document.getElementById("knownas");

        words = xhr.responseText.split(":");

        if (words[0] == "unknown") {
            p.textContent = "unknown! Go away."
        } else {
            p.textContent = words[0] + ". Cookie retrieved!";
            document.cookie = "auth_key=" + xhr.responseText;
        }
    };
    xhr.send('id_token=' + id_token);
}
