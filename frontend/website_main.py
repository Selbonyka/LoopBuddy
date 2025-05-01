from flask import Flask, views
from views import views
from datetime import timedelta

from secretkey import stored_secret_key # importing the secret key to hash user sessions


app = Flask(__name__)

app.register_blueprint(views, url_prefix="/")

# setting up sessions:
app.secret_key = stored_secret_key
app.config["SESSION_TYPE"] = "filesystem"
app.permanent_session_lifetime = timedelta(hours=2)

if __name__ == '__main__':
    app.run(debug=True, port=8000)