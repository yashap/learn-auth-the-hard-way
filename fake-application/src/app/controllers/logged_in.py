from flask import request, render_template, make_response
import requests
from werkzeug.exceptions import InternalServerError
from csrf.csrf import CSRFValidationError, is_uuid_v4, set_csrf_token


def get(app):
    code = request.args.get('code')
    csrf_token = request.args.get('state')
    if not is_uuid_v4(csrf_token):
        raise CSRFValidationError('CSRF token was not a uuid v4')
    # request.args.get('locale')
    # request.args.get('userState')
    base_url = 'http://host.docker.internal:9011/oauth2/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:8080/logged-in',
        'client_id': '746018f6-5765-4843-a31d-cce83303a552',
        'client_secret': 'HYPNsIZBusDEh5XwwvR3i_zLK7V6A0j6W9Kk89yfXAE'
    }
    token_response = requests.post(
        base_url,
        data=data
    )
    if token_response.status_code != 200:
        raise InternalServerError('Failed to get token')
    token_response_json = token_response.json()
    access_token = token_response_json.get('access_token')
    expires_in = token_response_json.get('expires_in')
    id_token = token_response_json.get('id_token')
    token_type = token_response_json.get('token_type')
    user_id = token_response_json.get('userId')
    app.logger.debug(
        'I should do something with this stuff.\naccess_token : %s\nexpires_in : %s\nid_token : %s\ntoken_type : %s\nuser_id: %s',
        access_token, expires_in, id_token, token_type, user_id
    )
    response = make_response(render_template('index.html'))
    set_csrf_token(response, csrf_token)
    return response
