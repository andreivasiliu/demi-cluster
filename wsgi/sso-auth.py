import logging
from flask import Flask, request, abort


app = Flask(__name__)
app.logger.setLevel(logging.INFO)


USERS = {
    '118382900112464632569': 'andrei',
    '117725485409166961892': 'costel',
}


@app.route("/get_cookie", methods=['POST'])
def get_cookie():
    from google.oauth2 import id_token
    from google.auth.transport import requests
    
    token = request.form['id_token']

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(),
            '131513390980-806sq81ev4ljmicqqedlbaf1df95gjp6.apps.googleusercontent.com'
        )

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
    except ValueError:
        # Invalid token
        userid = 'Unknown'

    user = USERS.get(userid)

    app.logger.info("Attempting to get auth key with: %s (%s)", userid, user or "unknown!")

    if not user:
        return "unknown"

    return "{}:{}".format(user, "secretkey")


@app.route("/check_auth", methods=['GET', 'POST'])
def check_auth():
    auth_key = request.cookies.get("auth_key")

    app.logger.info("Checking auth cookie: %s", auth_key)

    if not auth_key:
        app.logger.warn("Cannot authenticate: No cookie!")
        abort(401)

    user, _, key = auth_key.partition(':')

    if not key:
        app.logger.warn("Cannot authenticate: No key!")
        abort(401)

    if user not in USERS.values():
        app.logger.warn("Cannot authenticate: Unknown user!")
        abort(401)

    if key != "secretkey":
        app.logger.warn("Cannot authenticate: Incorrect key!")
        abort(401)

    return "Successfully authenticated as: {}".format(user)


@app.route("/key")
def key_info():
    with open("/var/demi/uwsgi/sso-auth/sso-auth.js") as f:
        script = f.read()
    
    with open('/var/demi/uwsgi/sso-auth/sso-auth.html') as f:
        page = f.read()
        
    return page.format(script=script)


@app.route("/")
def index():
    return "Nothing here!"


# This won't be executed when hosted by uwsgi
if __name__ == '__main__':
    app.run(host='0.0.0.0')
