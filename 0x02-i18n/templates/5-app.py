#!/usr/bin/env python3
"""Flask app with user login emulation"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _, lazy_gettext

app = Flask(__name__)
babel = Babel(app)

# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user(user_id):
    return users.get(user_id)

@app.before_request
def before_request():
    # Get user ID from the URL parameter
    user_id = request.args.get('login_as')

    # Set g.user to the user dictionary or None if not found
    g.user = get_user(int(user_id)) if user_id and user_id.isdigit() else None

@babel.localeselector
def get_locale():
    # Check if a user is logged in and has a preferred locale
    if g.user and 'locale' in g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    
    # Resort to the default behavior if not logged in or locale not supported
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    return render_template('5-index.html')

if __name__ == "__main__":
    app.run()
