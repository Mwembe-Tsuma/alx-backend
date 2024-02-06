#!/usr/bin/env python3
"""Flask app with forced locale support"""

from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)


class Config:
    """Config class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Loacle selector"""
    if 'locale' in request.args and request.args['locale'] in app.config['LANGUAGES']:
        return request.args['locale']

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Default route"""
    return render_template('4-index.html', title=_('home_title'), header=_('home_header'))


if __name__ == "__main__":
    app.run()
