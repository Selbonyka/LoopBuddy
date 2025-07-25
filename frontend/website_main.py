from flask import Flask, views
from views import views

from secretkey import stored_secret_key # importing the secret key to hash user sessions - should not be uploaded to github or such


app = Flask(__name__)

app.register_blueprint(views, url_prefix="/")

# setting up sessions:
app.secret_key = stored_secret_key
app.config["SESSION_TYPE"] = "filesystem"

if __name__ == '__main__':
    app.run(debug=True, port=8000)