#!/usr/bin/env python3
"""Flask app with user login emulation, improved locale, and timezone handling"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _, lazy_gettext
import pytz


app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """Users"""
    return users.get(user_id)


@app.before_request
def before_request():
    """Get user ID from the URL parameter"""
    user_id = request.args.get('login_as')

    g.user = get_user(int(user_id)) if user_id and user_id.isdigit() else None


@babel.localeselector
def get_locale():
    """Locale from URL parameters"""
    url_locale = request.args.get('locale')
    if url_locale and url_locale in app.config['LANGUAGES']:
        return url_locale

    if g.user and 'locale' in g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    request_locale = request.headers.get('Accept-Language')
    if request_locale:
        return request_locale.split(',')[0].split(';')[0]

    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """Timezone from URL parameters"""
    url_timezone = request.args.get('timezone')
    if url_timezone:
        try:
            pytz.timezone(url_timezone)
            return url_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user and 'timezone' in g.user:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    return 'UTC'


@app.route('/')
def index():
    """Default roor"""
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run()
