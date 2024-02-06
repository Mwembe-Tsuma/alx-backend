#!/usr/bin/env python3
"""Flask app with user login and preferred locale"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _, lazy_gettext


app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user(user_id):
    """Get user"""
    return users.get(user_id)


@app.before_request
def before_request():
    """Before request"""
    user_id = request.args.get('login_as')

    g.user = get_user(int(user_id)) if user_id and user_id.isdigit() else None


@babel.localeselector
def get_locale():
    """Locale selector"""
    if 'locale' in request.args and request.args['locale'] in app.config['LANGUAGES']:
        return request.args['locale']

    if g.user and 'locale' in g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    header_locale = request.headers.get('Accept-Language')
    if header_locale:
        for lang in app.config['LANGUAGES']:
            if lang in header_locale:
                return lang

    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/')
def index():
    """default root"""
    return render_template('6-index.html')


if __name__ == "__main__":
    app.run()
