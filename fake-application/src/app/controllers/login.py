from flask import redirect
from urllib.parse import urlencode
from csrf.csrf import get_csrf_token


def get(app):
    base_login_url = 'http://localhost:9011/oauth2/authorize'
    login_params = {
        'scope': 'openid profile email',
        'response_type': 'code',
        'client_id': '746018f6-5765-4843-a31d-cce83303a552',
        'redirect_uri': 'http://localhost:8080/logged-in',
        'state': get_csrf_token()
    }
    login_url = '{}?{}'.format(base_login_url, urlencode(login_params))
    app.logger.debug('Redirecting to %s', login_url)
    return redirect(login_url)
