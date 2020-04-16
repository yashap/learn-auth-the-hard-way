from flask import Flask, redirect, request, render_template
from flask_restful import Resource, Api
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from urllib.parse import urlencode
import os
import requests

SECRET_KEY = 'c50e7218-f5c6-41e0-8377-d9c57855cab6'

app = Flask(__name__)
app.secret_key = SECRET_KEY
csrf = CSRFProtect(app)
api = Api(app)

@app.before_request
def log_request_info():
    app.logger.debug(
        '%s %s%s\n%s',
        request.method,
        request.path,
        '?{}'.format(request.query_string) if request.query_string else '',
        str(request.headers).rstrip()
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logged-in')
def logged_in():
    code = request.args.get('code')
    # anti_forgery_token = request.args.get('state') # TODO: validate anti_forgery_token
    # request.args.get('locale')
    # request.args.get('userState')
    base_url = 'http://host.docker.internal:9011/oauth2/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:8080/logged-in'
    }
    token_response = requests.post(
        base_url,
        data=data,
        auth=('Basic', 'HYPNsIZBusDEh5XwwvR3i_zLK7V6A0j6W9Kk89yfXAE')
    ).json()
    # TODO: figure out who to auth properly
    app.logger.debug('\n\n\n>>>>>>>\nTOKEN RESPONSE:\n%s\n>>>>>>>', token_response)
    return render_template('index.html') # TODO: better page

@app.route('/logout')
def logout():
    return render_template('index.html') # TODO: better page

class LoginController(Resource):
    def get(self):
        login_url = self.__login_url()
        app.logger.debug('Redirecting to %s', login_url)
        return redirect(login_url)
    
    def __login_url(self):
        base_url = 'http://localhost:9011/oauth2/authorize'
        params = {
            'scope': 'openid profile email',
            'response_type': 'code',
            'client_id': '746018f6-5765-4843-a31d-cce83303a552',
            'redirect_uri': 'http://localhost:8080/logged-in',
            'state': generate_csrf()
        }
        return '{url}?{params}'.format(
            url=base_url,
            params=urlencode(params)
        )

class FooController(Resource):
    def post(self):
        app.logger.info('')
        return {}

api.add_resource(LoginController, '/login')
api.add_resource(FooController, '/foos')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
