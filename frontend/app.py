from flask import Flask
from routes.auth import auth_bp
from routes.polls import polls_bp

app = Flask(__name__)
app.secret_key = "enquetehub_secret_key"

app.register_blueprint(auth_bp)
app.register_blueprint(polls_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)