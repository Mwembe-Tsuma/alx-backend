#!/usr/bin/env python3
"""Basic Flask app"""

from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)
app.url_map.strict_slashes = False


class Config:
    """Configuration class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Local selector"""
    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/')
def index():
    """Default route"""
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(debug=True)
