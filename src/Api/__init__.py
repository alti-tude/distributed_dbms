from flask import Flask
from flask.helpers import url_for

app = Flask(__name__)

from .User import bp as user_bp
from .Internal import bp as internal_bp
from .Commit import bp as commit_bp

app.register_blueprint(user_bp)
app.register_blueprint(internal_bp)
app.register_blueprint(commit_bp)